.. _api:

API
===

.. currentmodule:: attr

``attrs`` works by decorating a class using :func:`attr.s` and then optionally defining attributes on the class using :func:`attr.ib`.

.. note::

   When this documentation speaks about "``attrs`` attributes" it means those attributes that are defined using :func:`attr.ib` in the class body.

What follows is the API explanation, if you'd like a more hands-on introduction, have a look at :doc:`examples`.



Core
----

.. autofunction:: attr.s(these=None, repr_ns=None, repr=True, cmp=True, hash=True, init=True, slots=False)

   .. note::

      ``attrs`` also comes with a less playful alias ``attr.attributes``.

   For example:

   .. doctest::

      >>> import attr
      >>> @attr.s
      ... class C(object):
      ...     _private = attr.ib()
      >>> C(private=42)
      C(_private=42)
      >>> class D(object):
      ...     def __init__(self, x):
      ...         self.x = x
      >>> D(1)
      <D object at ...>
      >>> D = attr.s(these={"x": attr.ib()}, init=False)(D)
      >>> D(1)
      D(x=1)


.. autofunction:: attr.ib

   .. note::

      ``attrs`` also comes with a less playful alias ``attr.attr``.


.. autoclass:: attr.Attribute

   Instances of this class are frequently used for introspection purposes like:

   - Class attributes on ``attrs``-decorated classes *after* ``@attr.s`` has been applied.
   - :func:`fields` returns a tuple of them.
   - Validators get them passed as the first argument.

   .. warning::

       You should never instantiate this class yourself!

   .. doctest::

      >>> import attr
      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      >>> C.x
      Attribute(name='x', default=NOTHING, validator=None, repr=True, cmp=True, hash=True, init=True, convert=None)


.. autofunction:: attr.make_class

   This is handy if you want to programmatically create classes.

   For example:

   .. doctest::

      >>> C1 = attr.make_class("C1", ["x", "y"])
      >>> C1(1, 2)
      C1(x=1, y=2)
      >>> C2 = attr.make_class("C2", {"x": attr.ib(default=42),
      ...                             "y": attr.ib(default=attr.Factory(list))})
      >>> C2()
      C2(x=42, y=[])


.. autoclass:: attr.Factory

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib(default=attr.Factory(list))
      >>> C()
      C(x=[])


Helpers
-------

``attrs`` comes with a bunch of helper methods that make the work with it easier:

.. autofunction:: attr.fields

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      ...     y = attr.ib()
      >>> attr.fields(C)
      (Attribute(name='x', default=NOTHING, validator=None, repr=True, cmp=True, hash=True, init=True, convert=None), Attribute(name='y', default=NOTHING, validator=None, repr=True, cmp=True, hash=True, init=True, convert=None))


.. autofunction:: attr.has

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     pass
      >>> attr.has(C)
      True
      >>> attr.has(object)
      False


.. autofunction:: attr.asdict

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      ...     y = attr.ib()
      >>> attr.asdict(C(1, C(2, 3)))
      {'y': {'y': 3, 'x': 2}, 'x': 1}


``attrs`` comes with some handy helpers for filtering:

.. autofunction:: attr.filters.include

.. autofunction:: attr.filters.exclude


.. autofunction:: assoc

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      ...     y = attr.ib()
      >>> i1 = C(1, 2)
      >>> i1
      C(x=1, y=2)
      >>> i2 = attr.assoc(i1, y=3)
      >>> i2
      C(x=1, y=3)
      >>> i1 == i2
      False


.. autofunction:: validate

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib(validator=attr.validators.instance_of(int))
      >>> i = C(1)
      >>> i.x = "1"
      >>> attr.validate(i)
      Traceback (most recent call last):
         ...
      TypeError: ("'x' must be <type 'int'> (got '1' that is a <type 'str'>).", Attribute(name='x', default=NOTHING, validator=<instance_of validator for type <type 'int'>>, repr=True, cmp=True, hash=True, init=True), <type 'int'>, '1')


Validators can be globally disabled if you want to run them only in development and tests but not in production because you fear their performance impact:

.. autofunction:: set_run_validators

.. autofunction:: get_run_validators


.. _api_validators:

Validators
----------

``attrs`` comes with some common validators within the ``attrs.validators`` module:


.. autofunction:: attr.validators.instance_of


   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib(validator=attr.validators.instance_of(int))
      >>> C(42)
      C(x=42)
      >>> C("42")
      Traceback (most recent call last):
         ...
      TypeError: ("'x' must be <type 'int'> (got '42' that is a <type 'str'>).", Attribute(name='x', default=NOTHING, validator=<instance_of validator for type <type 'int'>>), <type 'int'>, '42')
      >>> C(None)
      Traceback (most recent call last):
         ...
      TypeError: ("'x' must be <type 'int'> (got None that is a <type 'NoneType'>).", Attribute(name='x', default=NOTHING, validator=<instance_of validator for type <type 'int'>>, repr=True, cmp=True, hash=True, init=True), <type 'int'>, None)


.. autofunction:: attr.validators.provides

.. autofunction:: attr.validators.optional

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)))
      >>> C(42)
      C(x=42)
      >>> C("42")
      Traceback (most recent call last):
         ...
      TypeError: ("'x' must be <type 'int'> (got '42' that is a <type 'str'>).", Attribute(name='x', default=NOTHING, validator=<instance_of validator for type <type 'int'>>), <type 'int'>, '42')
      >>> C(None)
      C(x=None)
