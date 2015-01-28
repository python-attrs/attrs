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

.. autofunction:: attr.ib


Helpers
-------

``attrs`` comes with a bunch of helper methods that make the work with it easier:

.. autofunction:: attr.ls

   For example:

   .. doctest::

      >>> import attr
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

.. autoclass:: attr.Attribute

   This class is only interesting because it is returned by :func:`ls`.
