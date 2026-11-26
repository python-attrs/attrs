# SPDX-License-Identifier: MIT
# pyright: strict

"""
Classic API (attr.s / attr.ib) features.
"""

from __future__ import annotations

import re

from typing import Any

import attr
import attrs


@attr.s
class CC:
    a: int = attr.ib()


cc = CC(1)
CC(a=1)


@attr.s
class DD:
    x: list[int] = attr.ib()


@attr.s
class EE:
    y: "list[int]" = attr.ib()


@attr.s
class FF:
    z: Any = attr.ib()


@attr.s
class GG(DD):
    y: str = attr.ib()


GG(x=[1], y="foo")


@attr.s
class HH(DD, EE):
    z: float = attr.ib()


HH(x=[1], y=[], z=1.1)


@attr.s(auto_exc=True)
class Error(Exception):
    x: int = attr.ib()


try:
    raise Error(1)
except Error as e:
    e.x
    e.args
    str(e)


@attrs.define
class AliasExample:
    without_alias: int
    _with_alias: int = attr.ib(alias="_with_alias")


attr.fields(AliasExample).without_alias.alias
attr.fields(AliasExample)._with_alias.alias


@attr.s
class Validated:
    e: str = attr.ib(validator=attr.validators.matches_re(re.compile(r"foo")))
    f: str = attr.ib(
        validator=attr.validators.matches_re(r"foo", flags=42, func=re.search)
    )

    # Test different forms of instance_of
    g: int = attr.ib(validator=attr.validators.instance_of(int))
    h: int = attr.ib(validator=attr.validators.instance_of((int,)))
    j: int | str = attr.ib(validator=attr.validators.instance_of((int, str)))
    k: int | str | CC = attr.ib(
        validator=attrs.validators.instance_of((int, CC, str))
    )
    kk: int | str | CC = attr.ib(
        validator=attrs.validators.instance_of(int | CC | str)
    )

    l: Any = attr.ib(
        validator=attr.validators.not_(attr.validators.in_("abc"))
    )
    m: Any = attr.ib(
        validator=attr.validators.not_(
            attr.validators.in_("abc"), exc_types=ValueError
        )
    )
    n: Any = attr.ib(
        validator=attr.validators.not_(
            attr.validators.in_("abc"), exc_types=(ValueError,)
        )
    )
    o: Any = attr.ib(
        validator=attr.validators.not_(attr.validators.in_("abc"), msg="spam")
    )
    p: Any = attr.ib(
        validator=attr.validators.not_(attr.validators.in_("abc"), msg=None)
    )
    q: Any = attr.ib(
        validator=attrs.validators.optional(attrs.validators.instance_of(CC))
    )
    r: Any = attr.ib(
        validator=attrs.validators.optional([attrs.validators.instance_of(CC)])
    )
    s: Any = attr.ib(
        validator=attrs.validators.optional(
            (attrs.validators.instance_of(CC),)
        )
    )


@attr.s
class WithCustomRepr:
    a: int = attr.ib(repr=True)
    b: str = attr.ib(repr=False)
    c: str = attr.ib(repr=lambda value: "c is for cookie")
    d: bool = attr.ib(repr=str)


@attr.s(eq=True, order=False)
class OrderFlags:
    a: int = attr.ib(eq=False, order=False)
    b: int = attr.ib(eq=True, order=True)


@attr.s(on_setattr=attr.setters.validate)
class ValidatedSetter:
    a: int
    b: str = attr.ib(on_setattr=attr.setters.NO_OP)
    c: bool = attr.ib(on_setattr=attr.setters.frozen)
    d: int = attr.ib(on_setattr=[attr.setters.convert, attr.setters.validate])
    e: bool = attr.ib(
        on_setattr=attr.setters.pipe(
            attr.setters.convert, attr.setters.validate
        )
    )


# field_transformer
def ft_hook(
    cls: type, attribs: list[attr.Attribute[Any]]
) -> list[attr.Attribute[Any]]:
    return attribs


@attr.s(field_transformer=ft_hook)
class TransformedAttrs:
    x: int


@attr.s(auto_detect=True)
class AutoDetect:
    x: int

    def __init__(self, s: str):
        self.x = int(s)


@attr.s(collect_by_mro=True)
class MRO:
    pass


@attr.s
class FactoryTest:
    a: list[int] = attr.ib(  # pyright:ignore[reportUnknownVariableType]
        default=attr.Factory(list)  # pyright:ignore[reportUnknownArgumentType]
    )
    b: list[Any] = attr.ib(  # pyright:ignore[reportUnknownVariableType]
        default=attr.Factory(list, False)  # pyright:ignore[reportUnknownArgumentType]
    )
    c: list[int] = attr.ib(default=attr.Factory((lambda s: s.a), True))


@attr.s(match_args=False)
class MatchArgs:
    a: int = attr.ib()
    b: int = attr.ib()
