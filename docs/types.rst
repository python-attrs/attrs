Type Annotations
================

``attrs`` comes with first class support for type annotations for both Python 3.6 (:pep:`526`) and legacy syntax.

On Python 3.6 and later, you can even drop the `attr.ib`\ s if you're willing to annotate *all* attributes.
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

You will still need `attr.ib` for advanced features, but not for the common cases.

One of those features are the decorator-based features like defaults.
It's important to remember that ``attrs`` doesn't do any magic behind your back.
All the decorators are implemented using an object that is returned by the call to `attr.ib`.

Attributes that only carry a class annotation do not have that object so trying to call a method on it will inevitably fail.

*****

Please note that types -- however added -- are *only metadata* that can be queried from the class and they aren't used for anything out of the box!

Because Python does not allow references to a class object before the class is defined,
types may be defined as string literals, so-called *forward references*.
Also, starting in Python 3.10 (:pep:`526`) **all** annotations will be string literals.
When this happens, ``attrs`` will simply put these string literals into the ``type`` attributes.
If you need to resolve these to real types, you can call `attr.resolve_types` which will update the attribute in place.

In practice though, types show their biggest usefulness in combination with tools like mypy_, pytype_, or pyright_ that have dedicated support for ``attrs`` classes.

The addition of static types is certainly one of the most exciting features in the Python ecosystem and helps you writing *correct* and *verified self-documenting* code.

If you don't know where to start, Carl Meyer gave a great talk on `Type-checked Python in the Real World <https://www.youtube.com/watch?v=pMgmKJyWKn8>`_ at PyCon US 2018 that will help you to get started in no time.


mypy
----

While having a nice syntax for type metadata is great, it's even greater that mypy_ as of 0.570 ships with a dedicated ``attrs`` plugin which allows you to statically check your code.

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


pyright
-------

``attrs`` provides support for pyright_ though the dataclass_transform_ specification.
This provides static type inference for a subset of ``attrs`` equivalent to standard-library ``dataclasses``,
and requires explicit type annotations using the :ref:`next-gen` or ``@attr.s(auto_attribs=True)`` API.

Given the following definition, ``pyright`` will generate static type signatures for ``SomeClass`` attribute access, ``__init__``, ``__eq__``, and comparison methods::

  @attr.define
  class SomeClass:
      a_number: int = 42
      list_of_numbers: typing.List[int] = attr.field(factory=list)

.. warning::

   ``dataclass_transform``-based types are supported provisionally as of ``pyright`` 1.1.135 and ``attrs`` 21.1.
   Both the ``pyright`` dataclass_transform_ specification and ``attrs`` implementation may changed in future versions.

   The ``pyright`` inferred types are a subset of those supported by ``mypy``, including:

   - The generated ``__init__`` signature only includes the attribute type annotations.
     It currently does not include attribute ``converter`` types.

   - The ``attr.frozen`` decorator is not typed with frozen attributes, which are properly typed via ``attr.define(frozen=True)``.

   Your constructive feedback is welcome in both `attrs#795 <https://github.com/python-attrs/attrs/issues/795>`_ and `pyright#1782 <https://github.com/microsoft/pyright/discussions/1782>`_.


.. _mypy: http://mypy-lang.org
.. _pytype: https://google.github.io/pytype/
.. _pyright: https://github.com/microsoft/pyright
.. _dataclass_transform: https://github.com/microsoft/pyright/blob/master/specs/dataclass_transforms.md
