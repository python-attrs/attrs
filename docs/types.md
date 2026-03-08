# Type Annotations

The addition of static types is one of the most exciting features in the Python ecosystem and helps you write *correct* and *verified self-documenting* code.
*attrs* comes with first-class support for type annotations for both {pep}`526` and legacy syntax.

However, they will remain *optional* forever, therefore the example from the [README](https://github.com/python-attrs/attrs/blob/main/README.md) could also be written as:

```{doctest}
>>> from attrs import define, field

>>> @define
... class SomeClass:
...     a_number = field(default=42)
...     list_of_numbers = field(factory=list)

>>> sc = SomeClass(1, [1, 2, 3])
>>> sc
SomeClass(a_number=1, list_of_numbers=[1, 2, 3])
```

You can choose freely between the approaches, but remember that if you choose to use type annotations, you **must** annotate **all** attributes!

:::{caution}
If you define a class with a {func}`attrs.field` that **lacks** a type annotation, *attrs* will **ignore** other fields that have a type annotation, but are not defined using {func}`attrs.field`:

```{doctest}
>>> @define
... class SomeClass:
...     a_number = field(default=42)
...     another_number: int = 23
>>> SomeClass()
SomeClass(a_number=42)
```
:::

Even when going all-in on type annotations, you will need {func}`attrs.field` for some advanced features, though.

One of those features are decorator-based features like defaults.
It's important to remember that *attrs* doesn't do any magic behind your back here:
The decorators are implemented using an object that is returned by the call to {func}`attrs.field`.

Attributes that only carry a class annotation do not have that object so trying to call a method on it will inevitably fail.

---

Because Python does not allow references to a class object before the class is defined,
types may be defined as string literals, so-called *forward references* ({pep}`526`).
You can enable this automatically for a whole module by using `from __future__ import annotations` ({pep}`563`) or by running Python 3.14 or later.
In this case *attrs* simply puts these string literals into the `type` attributes[^314-str].
If you need to resolve these to real types, you can call {func}`attrs.resolve_types` which will update the attributes in place.

[^314-str]: It's not strings on 3.14 and later, but it's the same concept.


## Class variables and constants

Defining an attribute with a type annotation and assigned value looks like a class variable, but it isn't.
It's an instance variable with a default value.

The correct way to define a class variable is with {data}`typing.ClassVar`, which indicates that the variable should only be assigned in the class (or its subclasses) and not in instances of the class.
*attrs* will skip over members annotated with {data}`typing.ClassVar`, allowing you to write a type annotation without turning the member into an attribute.
Class variables are often used for constants, though they can also be used for mutable singleton data shared across all instances of the class.

```
@attrs.define
class PngHeader:
    SIGNATURE: typing.ClassVar[bytes] = b'\x89PNG\r\n\x1a\n'
    height: int
    width: int
    interlaced: int = 0
    ...
```


## Overview of type checkers

Types -- regardless how added -- are *only metadata* that can be queried from the class and they aren't used for anything out of the box.
So, in practice, types show their biggest usefulness in combination with type-checking tools or IDE support.

Over the years, the type-checking community has come up with {pep}`681` that defines `dataclass_transform` to offer a baseline way to define dataclass-like class generators.
All modern type-checking implementations support that, but in practice it's not enough to make the most out of *attrs*, so some offer further *attrs*-specific support.


### Mypy

[Mypy] is the original Python type checker and ships with a dedicated *attrs* plugin that implements our features far beyond {pep}`681`.

It also works with *both* legacy annotation styles.
With Mypy, you can also write this (but really shouldn't):

```python
@attr.s
class SomeClass:
    a_number = attr.ib(default=42)  # type: int
    list_of_numbers = attr.ib(factory=list, type=list[int])
```

The approach used for `list_of_numbers` one is only available in our [old-style API](names.md) which is why the example still uses it.


### Pyright

*attrs* integrates with Microsoft's [Pyright] via {pep}`681`.
While Pyright's not as commonly used as a type-checker, it's widely used as the foundation of VS Code's proprietary [Pylance](https://github.com/microsoft/pylance-release) language server that powers its Python support.

Pyright has grown several *attrs*-specific features over the years, but its inferred types are still a tiny subset of those supported by Mypy, including:

- Our auto-aliasing of private attributes is not supported.
  You have to manually tell Pyright about it: `_x: int = attrs.field(alias="x")`

- The `attrs.frozen` decorator is not typed with frozen attributes, which are properly typed via `attrs.define(frozen=True)`.

- None of the decorator-based features (like `@_x.default` or `@_x.validator`) are supported.

Your constructive feedback is welcome in both [attrs#795](https://github.com/python-attrs/attrs/issues/795) and [pyright#1782](https://github.com/microsoft/pyright/discussions/1782).
Keep in mind that the decision on improving *attrs* support in Pyright is entirely Microsoft's prerogative and they unequivocally indicated that they'll only add support for features that go through the PEP process.
We as the *attrs* project unfortunately have no influence over that.

Note that there's a community fork called [*basedpyright*](https://docs.basedpyright.com/) that implements some of Microsoft's closed-source Pylance features such that they're available in other editors like [Zed](https://zed.dev).
Unfortunately, better *attrs* support doesn't appear to be part of their goals.


### *ty*

[*ty*] is a fairly new Rust-based type checker from [Astral](https://astral.sh), the makers of Ruff and *uv*. 
Currently it only supports {pep}`681`, but [they intend]((https://github.com/astral-sh/ty/issues/2404)) to support more of *attrs*'s features.


### Pyrefly

[Pyrefly] is Meta's take on a Rust-based type checker for Python.
It also only implements {pep}`681` and based on the (lack of) activity on *attrs*-related issues on their bug tracker it doesn't seem like they have immediate ambition to do more than that at the moment.


[Mypy]: http://mypy-lang.org
[Pyright]: https://github.com/microsoft/pyright
[*ty*]: https://docs.astral.sh/ty/
[Pyrefly]: https://pyrefly.org/
