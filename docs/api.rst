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

.. autofunction:: attr.s(add_repr=True, add_cmp=True, add_hash=True, add_init=True)

   .. note::

      ``attrs`` also comes with a less playful alias ``attr.attributes``.

.. autofunction:: attr.ib

   .. note::

      ``attrs`` also comes with a less playful alias ``attr.attr``.


.. autoclass:: attr.Attribute

   Instances of this class are frequently used for introspection purposes like:

   - Class attributes on ``attrs``-decorated classes.
   - :func:`ls` returns a list of them.
   - Validators get them passed as the first argument.

   .. doctest::

      >>> import attr
      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      >>> C.x
      Attribute(name='x', default_value=NOTHING, default_factory=NOTHING, validator=None)


Helpers
-------

``attrs`` comes with a bunch of helper methods that make the work with it easier:

.. autofunction:: attr.ls

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      ...     y = attr.ib()
      >>> attr.ls(C)
      [Attribute(name='x', default_value=NOTHING, default_factory=NOTHING, validator=None), Attribute(name='y', default_value=NOTHING, default_factory=NOTHING, validator=None)]


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


.. autofunction:: attr.to_dict

   For example:

   .. doctest::

      >>> @attr.s
      ... class C(object):
      ...     x = attr.ib()
      ...     y = attr.ib()
      >>> attr.to_dict(C(1, C(2, 3)))
      {'y': {'y': 3, 'x': 2}, 'x': 1}


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
      TypeError: ("'x' must be <type 'int'> (got '42' that is a <type 'str'>).", Attribute(name='x', default_value=NOTHING, default_factory=NOTHING, validator=<instance_of validator for type <type 'int'>>), <type 'int'>, '42')
