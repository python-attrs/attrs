Type Annotations
================

``attrs`` comes with first class support for type annotations for both Python 3.6 (:pep:`526`) and legacy syntax.

On Python 3.6 and later, you can even drop the :func:`attr.ib`\ s if you're willing to annotate *all* attributes.
That means that on modern Python versions, the declaration part of the example from the README can be simplified to:


.. doctest::

   >>> import attr
   >>> import typing

   >>> @attr.s(auto_attribs=True)
   ... class SomeClass:
   ...     a_number: int = 42
   ...     list_of_numbers: typing.List[int] = attr.Factory(list)

   >>> sc = SomeClass(1, [1, 2, 3])
   >>> sc
   SomeClass(a_number=1, list_of_numbers=[1, 2, 3])
   >>> attr.fields(SomeClass).a_number.type
   <class 'int'>

You can still use :func:`attr.ib` for advanced features, but you don't have to.

Please note that these types are *only metadata* that can be queried from the class and they aren't used for anything out of the box!


mypy
----

While having a nice syntax for type metadata is great, it's even greater that `mypy <http://mypy-lang.org>`_ as of 0.570 ships with a dedicated ``attrs`` plugin which allows you to statically check your code.

Imagine you add another line that tries to instantiate the defined class using ``SomeClass("23")``.
Mypy will catch that error for you:

.. code-block:: console

   $ mypy t.py
   t.py:12: error: Argument 1 to "SomeClass" has incompatible type "str"; expected "int"

This happens *without* running your code!

And it also works with *both* Python 2-style annotation styles.
To mypy, this code is equivalent to the one above:

.. code-block:: python

  @attr.s
  class SomeClass(object):
      a_number = attr.ib(default=42)  # type: int
      list_of_numbers = attr.ib(factory=list, type=typing.List[int])

*****

The addition of static types is certainly one of the most exciting features in the Python ecosystem and helps you writing *correct* and *verified self-documenting* code.

If you don't know where to start, Carl Meyer gave a great talk on `Type-checked Python in the Real World <https://www.youtube.com/watch?v=pMgmKJyWKn8>`_ at PyCon US 2018 that will help you to get started in no time.
