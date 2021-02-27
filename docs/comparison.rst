Comparison
==========

By default, two instances of ``attrs`` classes are equal if all their fields are equal.
For that, ``attrs`` writes ``__eq__`` and ``__ne__`` methods for you.

Additionally, if you pass ``order=True`` (which is the default if you use the `attr.s` decorator), ``attrs`` will also create a full set of ordering methods that are based on the defined fields: ``__le__``, ``__lt__``, ``__ge__``, and ``__gt__``.


Customization
-------------

As with other features, you can exclude fields from being involved in comparison operations:

.. doctest::

   >>> import attr
   >>> @attr.s
   ... class C(object):
   ...     x = attr.ib()
   ...     y = attr.ib(eq=False)
   >>> C(1, 2) == C(1, 3)
   True

Additionally you can also pass a *callable* instead of a bool to both *eq* and *order*.
It is then used as a key function like you may know from `sorted`:

.. doctest::

   >>> import attr
   >>> @attr.s
   ... class S(object):
   ...     x = attr.ib(eq=str.lower)
   >>> S("foo") == S("FOO")
   True
   >>> @attr.s
   ... class C(object):
   ...     x = attr.ib(order=int)
   >>> C("10") > C("2")
   True

This is especially useful when you have fields with objects that have atypical comparison properties.
Common examples of such objects are `NumPy arrays <https://github.com/python-attrs/attrs/issues/435>`_.

Please note that *eq* and *order* are set *independently*, because *order* is `False` by default in `modern APIs <prov>`.
