.. _extending:

Extending
=========

Each ``attrs``-decorated class has a ``__attrs_attrs__`` class attribute.
It is a tuple of :class:`attr.Attribute` carrying meta-data about each attribute.

So it is fairly simple to build your own decorators on top of ``attrs``:

.. doctest::

   >>> import attr
   >>> def print_attrs(cls):
   ...     print(cls.__attrs_attrs__)
   >>> @print_attrs
   ... @attr.s
   ... class C(object):
   ...     a = attr.ib()
   (Attribute(name='a', default=NOTHING, validator=None, repr=True, cmp=True, hash=None, init=True, convert=None, metadata=mappingproxy({})),)


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
    >>> def typed(cls, default=attr.NOTHING, validator=None, repr=True, cmp=True, hash=None, init=True, convert=None, metadata={}):
    ...     metadata = dict() if not metadata else metadata
    ...     metadata[MY_TYPE_METADATA] = cls
    ...     return attr.ib(default, validator, repr, cmp, hash, init, convert, metadata)
    >>>
    >>> @attr.s
    ... class C(object):
    ...     x = typed(int, default=1, init=False)
    >>> attr.fields(C).x.metadata[MY_TYPE_METADATA]
    <class 'int'>
