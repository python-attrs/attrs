Extending
=========

Each ``attrs``-decorated class has a ``__attrs_attrs__`` class attribute.
It is a tuple of `attr.Attribute` carrying meta-data about each attribute.

So it is fairly simple to build your own decorators on top of ``attrs``:

.. doctest::

   >>> import attr
   >>> def print_attrs(cls):
   ...     print(cls.__attrs_attrs__)
   ...     return cls
   >>> @print_attrs
   ... @attr.s
   ... class C(object):
   ...     a = attr.ib()
   (Attribute(name='a', default=NOTHING, validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False, inherited=False, on_setattr=None),)


.. warning::

   The `attr.s` decorator **must** be applied first because it puts ``__attrs_attrs__`` in place!
   That means that is has to come *after* your decorator because::

      @a
      @b
      def f():
         pass

   is just `syntactic sugar <https://en.wikipedia.org/wiki/Syntactic_sugar>`_ for::

      def original_f():
         pass

      f = a(b(original_f))


Wrapping the Decorator
----------------------

A more elegant way can be to wrap ``attrs`` altogether and build a class `DSL <https://en.wikipedia.org/wiki/Domain-specific_language>`_ on top of it.

An example for that is the package `environ-config <https://github.com/hynek/environ-config>`_ that uses ``attrs`` under the hood to define environment-based configurations declaratively without exposing ``attrs`` APIs at all.

Another common use case is to overwrite ``attrs``'s defaults.

Unfortunately, this currently `confuses <https://github.com/python/mypy/issues/5406>`_ mypy's ``attrs`` plugin.
At the moment, the best workaround is to hold your nose, write a fake mypy plugin, and mutate a bunch of global variables::

   from mypy.plugin import Plugin
   from mypy.plugins.attrs import (
      attr_attrib_makers,
      attr_class_makers,
      attr_dataclass_makers,
   )

   # These work just like `attr.dataclass`.
   attr_dataclass_makers.add("my_module.method_looks_like_attr_dataclass")

   # This works just like `attr.s`.
   attr_class_makers.add("my_module.method_looks_like_attr_s")

   # These are our `attr.ib` makers.
   attr_attrib_makers.add("my_module.method_looks_like_attrib")

   class MyPlugin(Plugin):
       # Our plugin does nothing but it has to exist so this file gets loaded.
       pass


   def plugin(version):
       return MyPlugin


Then tell mypy about your plugin using your project's ``mypy.ini``:

.. code:: ini

   [mypy]
   plugins=<path to file>


.. warning::
   Please note that it is currently *impossible* to let mypy know that you've changed defaults like *eq* or *order*.
   You can only use this trick to tell mypy that a class is actually an ``attrs`` class.


Types
-----

``attrs`` offers two ways of attaching type information to attributes:

- `PEP 526 <https://www.python.org/dev/peps/pep-0526/>`_ annotations on Python 3.6 and later,
- and the *type* argument to `attr.ib`.

This information is available to you:

.. doctest::

   >>> import attr
   >>> @attr.s
   ... class C(object):
   ...     x: int = attr.ib()
   ...     y = attr.ib(type=str)
   >>> attr.fields(C).x.type
   <class 'int'>
   >>> attr.fields(C).y.type
   <class 'str'>

Currently, ``attrs`` doesn't do anything with this information but it's very useful if you'd like to write your own validators or serializers!


.. _extending_metadata:

Metadata
--------

If you're the author of a third-party library with ``attrs`` integration, you may want to take advantage of attribute metadata.

Here are some tips for effective use of metadata:

- Try making your metadata keys and values immutable.
  This keeps the entire ``Attribute`` instances immutable too.

- To avoid metadata key collisions, consider exposing your metadata keys from your modules.::

    from mylib import MY_METADATA_KEY

    @attr.s
    class C(object):
      x = attr.ib(metadata={MY_METADATA_KEY: 1})

  Metadata should be composable, so consider supporting this approach even if you decide implementing your metadata in one of the following ways.

- Expose ``attr.ib`` wrappers for your specific metadata.
  This is a more graceful approach if your users don't require metadata from other libraries.

  .. doctest::

    >>> MY_TYPE_METADATA = '__my_type_metadata'
    >>>
    >>> def typed(
    ...     cls, default=attr.NOTHING, validator=None, repr=True,
    ...     eq=True, order=None, hash=None, init=True, metadata={},
    ...     type=None, converter=None
    ... ):
    ...     metadata = dict() if not metadata else metadata
    ...     metadata[MY_TYPE_METADATA] = cls
    ...     return attr.ib(
    ...         default=default, validator=validator, repr=repr,
    ...         eq=eq, order=order, hash=hash, init=init,
    ...         metadata=metadata, type=type, converter=converter
    ...     )
    >>>
    >>> @attr.s
    ... class C(object):
    ...     x = typed(int, default=1, init=False)
    >>> attr.fields(C).x.metadata[MY_TYPE_METADATA]
    <class 'int'>


.. _transform-fields:

Automatic Field Transformation and Modification
-----------------------------------------------

``attrs`` allows you to automatically modify or transform the class' fields while the class is being created.
You do this by passing a *field_transformer* hook to `attr.define` (and its friends).
Its main purpose is to automatically add converters to attributes based on their type to aid the development of API clients and other typed data loaders.

This hook must have the following signature:

.. function:: your_hook(cls: type, fields: List[attr.Attribute]) -> List[attr.Attribute]
   :noindex:

- *cls* is your class right *before* it is being converted into an attrs class.
  This means it does not yet have the ``__attrs_attrs__`` attribute.

- *fields* is a list of all :class:`attr.Attribute` instances that will later be set to ``__attrs_attrs__``.
  You can modify these attributes any way you want:
  You can add converters, change types, and even remove attributes completely or create new ones!

For example, let's assume that you really don't like floats:

.. doctest::

   >>> def drop_floats(cls, fields):
   ...     return [f for f in fields if f.type not in {float, 'float'}]
   ...
   >>> @attr.frozen(field_transformer=drop_floats)
   ... class Data:
   ...     a: int
   ...     b: float
   ...     c: str
   ...
   >>> Data(42, "spam")
   Data(a=42, c='spam')

A more realistic example would be to automatically convert data that you, e.g., load from JSON:

.. doctest::

   >>> from datetime import datetime
   >>>
   >>> def auto_convert(cls, fields):
   ...     results = []
   ...     for field in fields:
   ...         if field.converter is not None:
   ...             results.append(field)
   ...             continue
   ...         if field.type in {datetime, 'datetime'}:
   ...             converter = (lambda d: datetime.fromisoformat(d) if isinstance(d, str) else d)
   ...         else:
   ...             converter = None
   ...         results.append(field.evolve(converter=converter))
   ...     return results
   ...
   >>> @attr.frozen(field_transformer=auto_convert)
   ... class Data:
   ...     a: int
   ...     b: str
   ...     c: datetime
   ...
   >>> from_json = {"a": 3, "b": "spam", "c": "2020-05-04T13:37:00"}
   >>> Data(**from_json)  # ****
   Data(a=3, b='spam', c=datetime.datetime(2020, 5, 4, 13, 37))


Customize Value Serialization in ``asdict()``
---------------------------------------------

``attrs`` allows you to serialize instances of ``attrs`` classes to dicts using the `attr.asdict` function.
However, the result can not always be serialized since most data types will remain as they are:

.. doctest::

   >>> import json
   >>> import datetime
   >>>
   >>> @attr.frozen
   ... class Data:
   ...    dt: datetime.datetime
   ...
   >>> data = attr.asdict(Data(datetime.datetime(2020, 5, 4, 13, 37)))
   >>> data
   {'dt': datetime.datetime(2020, 5, 4, 13, 37)}
   >>> json.dumps(data)
   Traceback (most recent call last):
     ...
   TypeError: Object of type datetime is not JSON serializable

To help you with this, `attr.asdict` allows you to pass a *value_serializer* hook.
It has the signature

.. function:: your_hook(inst: type, field: attr.Attribute, value: typing.Any) -> typing.Any
   :noindex:

.. doctest::

   >>> def serialize(inst, field, value):
   ...     if isinstance(value, datetime.datetime):
   ...         return value.isoformat()
   ...     return value
   ...
   >>> data = attr.asdict(
   ...     Data(datetime.datetime(2020, 5, 4, 13, 37)),
   ...     value_serializer=serialize,
   ... )
   >>> data
   {'dt': '2020-05-04T13:37:00'}
   >>> json.dumps(data)
   '{"dt": "2020-05-04T13:37:00"}'
