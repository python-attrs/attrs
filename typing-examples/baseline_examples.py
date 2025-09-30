# SPDX-License-Identifier: MIT
# pyright: strict

"""
Baseline features that should be supported by all type checkers.
"""

from __future__ import annotations

from typing import Any

import attrs


@attrs.define(order=True)
class NGClass:
    x: int = attrs.field(default=42)


ngc = NGClass(1)


@attrs.mutable(slots=False)
class NGClass2:
    x: int


ngc2 = NGClass2(1)


@attrs.frozen(str=True)
class NGFrozen:
    x: int


ngf = NGFrozen(1)

attrs.fields(NGFrozen).x.evolve(eq=False)
a = attrs.fields(NGFrozen).x
a.evolve(repr=False)


@attrs.define
class C:
    a: int


c = C(1)
c.a


@attrs.frozen
class D:
    a: int


D(1).a


@attrs.define
class Derived(C):
    b: int


Derived(1, 2).a
Derived(1, 2).b


@attrs.define
class Error(Exception):
    x: int


try:
    raise Error(1)
except Error as e:
    e.x
    e.args
    str(e)


@attrs.define
class AliasExample:
    without_alias: int
    _with_alias: int = attrs.field(alias="_with_alias")


attrs.fields(AliasExample).without_alias.alias
attrs.fields(AliasExample)._with_alias.alias


@attrs.define
class Validated:
    num: int = attrs.field(validator=attrs.validators.ge(0))


@attrs.define
class ValidatedInconsistentOr:
    num: int | str = attrs.field(
        validator=attrs.validators.or_(
            # Various types of validators.
            attrs.validators.ge(0),
            attrs.validators.instance_of(str),
        )
    )


attrs.validators.set_disabled(True)
attrs.validators.set_disabled(False)


with attrs.validators.disabled():
    Validated(num=-1)


@attrs.define
class WithCustomRepr:
    a: int = attrs.field(repr=True)
    b: str = attrs.field(repr=False)
    c: str = attrs.field(repr=lambda value: "c is for cookie")
    d: bool = attrs.field(repr=str)


@attrs.define(on_setattr=attrs.setters.validate)
class ValidatedSetter2:
    a: int
    b: str = attrs.field(on_setattr=attrs.setters.NO_OP)
    c: bool = attrs.field(on_setattr=attrs.setters.frozen)
    d: int = attrs.field(
        on_setattr=[attrs.setters.convert, attrs.setters.validate]
    )
    e: bool = attrs.field(
        on_setattr=attrs.setters.pipe(
            attrs.setters.convert, attrs.setters.validate
        )
    )


@attrs.define(eq=True, order=True)
class OrderFlags:
    a: int = attrs.field(eq=False, order=False)
    b: int = attrs.field(eq=True, order=True)


# field_transformer
def ft_hook2(
    cls: type, attribs: list[attrs.Attribute[Any]]
) -> list[attrs.Attribute[Any]]:
    return attribs


@attrs.define(field_transformer=ft_hook2)
class TransformedAttrs2:
    x: int


@attrs.define
class FactoryTest:
    a: list[int] = attrs.field(factory=list)  # pyright:ignore[reportUnknownVariableType]
    b: list[str] = attrs.field(  # pyright:ignore[reportUnknownVariableType]
        default=attrs.Factory(list, takes_self=False)  # pyright:ignore[reportUnknownArgumentType]
    )
    c: list[int] = attrs.field(default=attrs.Factory((lambda s: s.a), True))
    d: list[int] = attrs.Factory(list)  # pyright:ignore[reportUnknownVariableType]


attrs.asdict(FactoryTest())
attrs.asdict(FactoryTest(), retain_collection_types=False)


@attrs.define(match_args=False)
class MatchArgs2:
    a: int
    b: int


# NG versions of asdict/astuple
attrs.asdict(MatchArgs2(1, 2))
attrs.astuple(MatchArgs2(1, 2))


def accessing_from_attrs() -> None:
    """
    Use a function to keep the ns clean.
    """
    attrs.converters.optional
    attrs.exceptions.FrozenError
    attrs.filters.include
    attrs.filters.exclude
    attrs.setters.frozen
    attrs.validators.and_
    attrs.cmp_using


@attrs.define(unsafe_hash=True)
class Hashable:
    pass


cp: attrs.ClassProps = attrs.inspect(Hashable)
cp.added_init
if cp.hashability is attrs.ClassProps.Hashability.UNHASHABLE:
    cp.is_slotted


def test(cls: type) -> None:
    if attrs.has(cls):
        attrs.resolve_types(cls)
