.. _extending:

Extending
=========

Each ``attrs``-decorated class has a ``__attrs_attrs__`` class attribute.
It is a tuple of :class:`attr.Attribute` carrying meta-data about each attribute.

So it is fairly simple to build your own decorators on top of ``attrs``:

.. doctest::

   >>> import attr
   >>> def print_attrs(cl):
   ...     print(cl.__attrs_attrs__)
   >>> @print_attrs
   ... @attr.s
   ... class C(object):
   ...     a = attr.ib()
   (Attribute(name='a', default=NOTHING, validator=None, repr=True, cmp=True, hash=True, init=True, convert=None),)


.. warning::

   The :func:`attr.s` decorator **must** be applied first because it puts ``__attrs_attrs__`` in place!
   That means that is has to come *after* your decorator because::

      @a
      @b
      def f():
         pass

   is just `syntactic sugar <https://en.wikipedia.org/wiki/Syntactic_sugar>`_ for::

      def original_f():
         pass

      f = a(b(original_f))
