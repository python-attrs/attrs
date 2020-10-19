API Reference
=============

.. currentmodule:: attr

``attrs`` works by decorating a class using `attr.s` and then optionally defining attributes on the class using `attr.ib`.

.. note::

   When this documentation speaks about "``attrs`` attributes" it means those attributes that are defined using `attr.ib` in the class body.

What follows is the API explanation, if you'd like a more hands-on introduction, have a look at `examples`.



Core
----


.. warning::
   As of ``attrs`` 20.1.0, it also ships with a bunch of provisional APIs that are intended to become the main way of defining classes in the future.

   Please have a look at :ref:`prov`.

.. autodata:: attr.NOTHING

.. autofunction:: attr.s(these=None, repr_ns=None, repr=None, cmp=None, hash=None, init=None, slots=False, frozen=False, weakref_slot=True, str=False, auto_attribs=False, kw_only=False, cache_hash=False, auto_exc=False, eq=None, order=None, auto_detect=False, collect_by_mro=False, getstate_setstate=None, on_setattr=None, field_transformer=None)

   .. note::

      ``attrs`` also comes with a serious business alias ``attr.attrs``.

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
      >>> @attr.s(auto_exc=True)
      ... class Error(Exception):
      ...     x = attr.ib()
      ...     y = attr.ib(default=42, init=False)
      >>> Error("foo")
      Error(x='foo', y=42)
      >>> raise Error("foo")
      Traceback (most recent call last):
         ...
      Error: ('foo', 42)
      >>> raise ValueError("foo", 42)   # for comparison
      Traceback (most recent call last):
         ...
      ValueError: ('foo', 42)


.. autofunction:: attr.ib

   .. note::

      ``attrs`` also comes with a serious business alias ``attr.attrib``.

   The object returned by `attr.ib` also allows for setting the default and the validator using decorators:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      ...     y = attr.ib()
      ...     @x.validator
      ...     def _any_name_except_a_name_of_an_attribute(self, attribute, value):
      ...         if value < 0:
      ...             raise ValueError("x must be positive")
      ...     @y.default
      ...     def _any_name_except_a_name_of_an_attribute(self):
      ...         return self.x + 1
      >>> C(1)
      C(x=1, y=2)
      >>> C(-1)
      Traceback (most recent call last):
          ...
      ValueError: x must be positive

.. autoclass:: attr.Attribute
   :members: evolve

   .. doctest::

      >>> import attr
      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      >>> attr.fields(C).x
      Attribute(name='x', default=NOTHING, validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False, inherited=False, on_setattr=None)


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
      ...     y = attr.ib(default=attr.Factory(
      ...         lambda self: set(self.x),
      ...         takes_self=True)
      ...     )
      >>> C()
      C(x=[], y=set())
      >>> C([1, 2, 3])
      C(x=[1, 2, 3], y={1, 2, 3})


Exceptions
----------

.. autoexception:: attr.exceptions.PythonTooOldError
.. autoexception:: attr.exceptions.FrozenError
.. autoexception:: attr.exceptions.FrozenInstanceError
.. autoexception:: attr.exceptions.FrozenAttributeError
.. autoexception:: attr.exceptions.AttrsAttributeNotFoundError
.. autoexception:: attr.exceptions.NotAnAttrsClassError
.. autoexception:: attr.exceptions.DefaultAlreadySetError
.. autoexception:: attr.exceptions.UnannotatedAttributeError
.. autoexception:: attr.exceptions.NotCallableError

   For example::

       @attr.s(auto_attribs=True)
       class C:
           x: int
           y = attr.ib()  # <- ERROR!


.. _helpers:

Helpers
-------

``attrs`` comes with a bunch of helper methods that make working with it easier:

.. autofunction:: attr.fields

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      ...     y = attr.ib()
      >>> attr.fields(C)
      (Attribute(name='x', default=NOTHING, validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False, inherited=False, on_setattr=None), Attribute(name='y', default=NOTHING, validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False, inherited=False, on_setattr=None))
      >>> attr.fields(C)[1]
      Attribute(name='y', default=NOTHING, validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False, inherited=False, on_setattr=None)
      >>> attr.fields(C).y is attr.fields(C)[1]
      True

.. autofunction:: attr.fields_dict

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      ...     y = attr.ib()
      >>> attr.fields_dict(C)
      {'x': Attribute(name='x', default=NOTHING, validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False, inherited=False, on_setattr=None), 'y': Attribute(name='y', default=NOTHING, validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False, inherited=False, on_setattr=None)}
      >>> attr.fields_dict(C)['y']
      Attribute(name='y', default=NOTHING, validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False, inherited=False, on_setattr=None)
      >>> attr.fields_dict(C)['y'] is attr.fields(C).y
      True


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


.. autofunction:: attr.resolve_types

    For example:

    .. doctest::

        >>> import typing
        >>> @attr.s(auto_attribs=True)
        ... class A:
        ...     a: typing.List['A']
        ...     b: 'B'
        ...
        >>> @attr.s(auto_attribs=True)
        ... class B:
        ...     a: A
        ...
        >>> attr.fields(A).a.type
        typing.List[ForwardRef('A')]
        >>> attr.fields(A).b.type
        'B'
        >>> attr.resolve_types(A, globals(), locals())
        <class 'A'>
        >>> attr.fields(A).a.type
        typing.List[A]
        >>> attr.fields(A).b.type
        <class 'B'>

.. autofunction:: attr.asdict

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      ...     y = attr.ib()
      >>> attr.asdict(C(1, C(2, 3)))
      {'x': 1, 'y': {'x': 2, 'y': 3}}


.. autofunction:: attr.astuple

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      ...     y = attr.ib()
      >>> attr.astuple(C(1,2))
      (1, 2)

``attrs`` includes some handy helpers for filtering the attributes in `attr.asdict` and `attr.astuple`:

.. autofunction:: attr.filters.include

.. autofunction:: attr.filters.exclude

See :func:`asdict` for examples.

.. autofunction:: attr.evolve

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      ...     y = attr.ib()
      >>> i1 = C(1, 2)
      >>> i1
      C(x=1, y=2)
      >>> i2 = attr.evolve(i1, y=3)
      >>> i2
      C(x=1, y=3)
      >>> i1 == i2
      False

   ``evolve`` creates a new instance using ``__init__``.
   This fact has several implications:

   * private attributes should be specified without the leading underscore, just like in ``__init__``.
   * attributes with ``init=False`` can't be set with ``evolve``.
   * the usual ``__init__`` validators will validate the new values.

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
      TypeError: ("'x' must be <class 'int'> (got '1' that is a <class 'str'>).", ...)


Validators can be globally disabled if you want to run them only in development and tests but not in production because you fear their performance impact:

.. autofunction:: set_run_validators

.. autofunction:: get_run_validators


.. _api_validators:

Validators
----------

``attrs`` comes with some common validators in the ``attrs.validators`` module:


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
      TypeError: ("'x' must be <type 'int'> (got '42' that is a <type 'str'>).", Attribute(name='x', default=NOTHING, validator=<instance_of validator for type <type 'int'>>, type=None, kw_only=False), <type 'int'>, '42')
      >>> C(None)
      Traceback (most recent call last):
         ...
      TypeError: ("'x' must be <type 'int'> (got None that is a <type 'NoneType'>).", Attribute(name='x', default=NOTHING, validator=<instance_of validator for type <type 'int'>>, repr=True, cmp=True, hash=None, init=True, type=None, kw_only=False), <type 'int'>, None)

.. autofunction:: attr.validators.in_

   For example:

   .. doctest::

       >>> import enum
       >>> class State(enum.Enum):
       ...     ON = "on"
       ...     OFF = "off"
       >>> @attr.s
       ... class C(object):
       ...     state = attr.ib(validator=attr.validators.in_(State))
       ...     val = attr.ib(validator=attr.validators.in_([1, 2, 3]))
       >>> C(State.ON, 1)
       C(state=<State.ON: 'on'>, val=1)
       >>> C("on", 1)
       Traceback (most recent call last):
          ...
       ValueError: 'state' must be in <enum 'State'> (got 'on')
       >>> C(State.ON, 4)
       Traceback (most recent call last):
          ...
       ValueError: 'val' must be in [1, 2, 3] (got 4)

.. autofunction:: attr.validators.provides

.. autofunction:: attr.validators.and_

   For convenience, it's also possible to pass a list to `attr.ib`'s validator argument.

   Thus the following two statements are equivalent::

      x = attr.ib(validator=attr.validators.and_(v1, v2, v3))
      x = attr.ib(validator=[v1, v2, v3])

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
      TypeError: ("'x' must be <type 'int'> (got '42' that is a <type 'str'>).", Attribute(name='x', default=NOTHING, validator=<instance_of validator for type <type 'int'>>, type=None, kw_only=False), <type 'int'>, '42')
      >>> C(None)
      C(x=None)


.. autofunction:: attr.validators.is_callable

    For example:

    .. doctest::

        >>> @attr.s
        ... class C(object):
        ...     x = attr.ib(validator=attr.validators.is_callable())
        >>> C(isinstance)
        C(x=<built-in function isinstance>)
        >>> C("not a callable")
        Traceback (most recent call last):
            ...
        attr.exceptions.NotCallableError: 'x' must be callable (got 'not a callable' that is a <class 'str'>).


.. autofunction:: attr.validators.matches_re

    For example:

    .. doctest::

        >>> @attr.s
        ... class User(object):
        ...     email = attr.ib(validator=attr.validators.matches_re(
        ...         "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        >>> User(email="user@example.com")
        User(email='user@example.com')
        >>> User(email="user@example.com@test.com")
        Traceback (most recent call last):
            ...
        ValueError: ("'email' must match regex '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\\\.[a-zA-Z0-9-.]+$)' ('user@example.com@test.com' doesn't)", Attribute(name='email', default=NOTHING, validator=<matches_re validator for pattern re.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)')>, repr=True, cmp=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False), re.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)'), 'user@example.com@test.com')


.. autofunction:: attr.validators.deep_iterable

    For example:

    .. doctest::

        >>> @attr.s
        ... class C(object):
        ...     x = attr.ib(validator=attr.validators.deep_iterable(
        ...     member_validator=attr.validators.instance_of(int),
        ...     iterable_validator=attr.validators.instance_of(list)
        ...     ))
        >>> C(x=[1, 2, 3])
        C(x=[1, 2, 3])
        >>> C(x=set([1, 2, 3]))
        Traceback (most recent call last):
            ...
        TypeError: ("'x' must be <class 'list'> (got {1, 2, 3} that is a <class 'set'>).", Attribute(name='x', default=NOTHING, validator=<deep_iterable validator for <instance_of validator for type <class 'list'>> iterables of <instance_of validator for type <class 'int'>>>, repr=True, cmp=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False), <class 'list'>, {1, 2, 3})
        >>> C(x=[1, 2, "3"])
        Traceback (most recent call last):
            ...
        TypeError: ("'x' must be <class 'int'> (got '3' that is a <class 'str'>).", Attribute(name='x', default=NOTHING, validator=<deep_iterable validator for <instance_of validator for type <class 'list'>> iterables of <instance_of validator for type <class 'int'>>>, repr=True, cmp=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False), <class 'int'>, '3')


.. autofunction:: attr.validators.deep_mapping

    For example:

    .. doctest::

        >>> @attr.s
        ... class C(object):
        ...     x = attr.ib(validator=attr.validators.deep_mapping(
        ...         key_validator=attr.validators.instance_of(str),
        ...         value_validator=attr.validators.instance_of(int),
        ...         mapping_validator=attr.validators.instance_of(dict)
        ...     ))
        >>> C(x={"a": 1, "b": 2})
        C(x={'a': 1, 'b': 2})
        >>> C(x=None)
        Traceback (most recent call last):
            ...
        TypeError: ("'x' must be <class 'dict'> (got None that is a <class 'NoneType'>).", Attribute(name='x', default=NOTHING, validator=<deep_mapping validator for objects mapping <instance_of validator for type <class 'str'>> to <instance_of validator for type <class 'int'>>>, repr=True, cmp=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False), <class 'dict'>, None)
        >>> C(x={"a": 1.0, "b": 2})
        Traceback (most recent call last):
            ...
        TypeError: ("'x' must be <class 'int'> (got 1.0 that is a <class 'float'>).", Attribute(name='x', default=NOTHING, validator=<deep_mapping validator for objects mapping <instance_of validator for type <class 'str'>> to <instance_of validator for type <class 'int'>>>, repr=True, cmp=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False), <class 'int'>, 1.0)
        >>> C(x={"a": 1, 7: 2})
        Traceback (most recent call last):
            ...
        TypeError: ("'x' must be <class 'str'> (got 7 that is a <class 'int'>).", Attribute(name='x', default=NOTHING, validator=<deep_mapping validator for objects mapping <instance_of validator for type <class 'str'>> to <instance_of validator for type <class 'int'>>>, repr=True, cmp=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False), <class 'str'>, 7)


Converters
----------

.. autofunction:: attr.converters.pipe

   For convenience, it's also possible to pass a list to `attr.ib`'s converter argument.

   Thus the following two statements are equivalent::

      x = attr.ib(converter=attr.converter.pipe(c1, c2, c3))
      x = attr.ib(converter=[c1, c2, c3])

.. autofunction:: attr.converters.optional

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib(converter=attr.converters.optional(int))
      >>> C(None)
      C(x=None)
      >>> C(42)
      C(x=42)


.. autofunction:: attr.converters.default_if_none

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib(
      ...         converter=attr.converters.default_if_none("")
      ...     )
      >>> C(None)
      C(x='')


.. _api_setters:

Setters
-------

These are helpers that you can use together with `attr.s`'s and `attr.ib`'s ``on_setattr`` arguments.

.. autofunction:: attr.setters.frozen
.. autofunction:: attr.setters.validate
.. autofunction:: attr.setters.convert
.. autofunction:: attr.setters.pipe
.. autodata:: attr.setters.NO_OP

   For example, only ``x`` is frozen here:

   .. doctest::

     >>> @attr.s(on_setattr=attr.setters.frozen)
     ... class C(object):
     ...     x = attr.ib()
     ...     y = attr.ib(on_setattr=attr.setters.NO_OP)
     >>> c = C(1, 2)
     >>> c.y = 3
     >>> c.y
     3
     >>> c.x = 4
     Traceback (most recent call last):
         ...
     attr.exceptions.FrozenAttributeError: ()

   N.B. Please use `attr.s`'s *frozen* argument to freeze whole classes; it is more efficient.


.. _prov:

Provisional APIs
----------------

These are Python 3.6 and later-only, keyword-only, and **provisional** APIs that call `attr.s` with different default values.

The most notable differences are:

- automatically detect whether or not *auto_attribs* should be `True`
- *slots=True*  (see :term:`slotted classes` for potentially surprising behaviors)
- *auto_exc=True*
- *auto_detect=True*
- *eq=True*, but *order=False*
- Validators run when you set an attribute (*on_setattr=attr.setters.validate*).
- Some options that aren't relevant to Python 3 have been dropped.

Please note that these are *defaults* and you're free to override them, just like before.

----

Their behavior is scheduled to become part of the upcoming ``import attrs`` that will introduce a new namespace  with nicer names and nicer defaults (see  `#408 <https://github.com/python-attrs/attrs/issues/408>`_ and `#487 <https://github.com/python-attrs/attrs/issues/487>`_).

Therefore your constructive feedback in the linked issues above is strongly encouraged!

.. note::
   Provisional doesn't mean we will remove it (although it will be deprecated once the final form is released), but that it might change if we receive relevant feedback.

   `attr.s` and `attr.ib` (and their serious business cousins) aren't going anywhere.
   The new APIs build on top of them.

.. autofunction:: attr.define
.. function:: attr.mutable(same_as_define)

   Alias for `attr.define`.

   .. versionadded:: 20.1.0

.. function:: attr.frozen(same_as_define)

   Behaves the same as `attr.define` but sets *frozen=True* and *on_setattr=None*.

   .. versionadded:: 20.1.0

.. autofunction:: attr.field


Deprecated APIs
---------------

.. _version-info:

To help you write backward compatible code that doesn't throw warnings on modern releases, the ``attr`` module has an ``__version_info__`` attribute as of version 19.2.0.
It behaves similarly to `sys.version_info` and is an instance of `VersionInfo`:

.. autoclass:: VersionInfo

   With its help you can write code like this:

   >>> if getattr(attr, "__version_info__", (0,)) >= (19, 2):
   ...     cmp_off = {"eq": False}
   ... else:
   ...     cmp_off = {"cmp": False}
   >>> cmp_off == {"eq":  False}
   True
   >>> @attr.s(**cmp_off)
   ... class C(object):
   ...     pass


----

The serious business aliases used to be called ``attr.attributes`` and ``attr.attr``.
There are no plans to remove them but they shouldn't be used in new code.

The ``cmp`` argument to both `attr.s` and `attr.ib` has been deprecated in 19.2 and shouldn't be used.

.. autofunction:: assoc
