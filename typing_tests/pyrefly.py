# SPDX-License-Identifier: MIT

"""
Typing examples that rely on Pyrefly's advanced attrs integration.
"""

from __future__ import annotations

import copy
import re
import sys

from typing import Any

import attrs


@attrs.define
class C:
    a: int = attrs.field()


cc = C(1)
C(a=1)

if sys.version_info >= (3, 13):
    cc = copy.replace(cc, x=1)


@attrs.define
class D:
    x: list[int] = attrs.field()


li: list[int] = D([1]).x


@attrs.define
class E:
    y: "list[int]" = attrs.field()


li = E([1]).y


@attrs.define
class F:
    z: Any = attrs.field()


# Inheritance --


@attrs.define
class GG(D):
    y: str = attrs.field()


GG(x=[1], y="foo")


@attrs.define
class HH(D, E):
    z: float = attrs.field()


HH(x=[1], y=[], z=1.1)


# Exceptions
@attrs.define
class Error(Exception):
    x: int = attrs.field()


try:
    raise Error(1)
except Error as e:
    e.x
    e.args
    str(e)


@attrs.define(auto_exc=False)
class Error2(Exception):
    x: int


try:
    raise Error2(1)
except Error as e:
    e.x
    e.args
    str(e)

# Field aliases


@attrs.define
class AliasExample:
    without_alias: int
    _with_alias: int = attrs.field(alias="_with_alias")


attrs.fields(AliasExample).without_alias.alias
attrs.fields(AliasExample)._with_alias.alias


# Converters


@attrs.define
class ConvCOptional:
    x: int | None = attrs.field(converter=attrs.converters.optional(int))


ConvCOptional(1)
ConvCOptional(None)


@attrs.define
class ConvCPipe:
    x: str = attrs.field(converter=attrs.converters.pipe(int, str))


ConvCPipe(3.4)
ConvCPipe("09")


@attrs.define
class ConvCDefaultIfNone:
    x: int = attrs.field(converter=attrs.converters.default_if_none(42))


ConvCDefaultIfNone(1)
ConvCDefaultIfNone(None)


@attrs.define
class ConvCToBool:
    x: int = attrs.field(converter=attrs.converters.to_bool)


ConvCToBool(1)
ConvCToBool(True)
ConvCToBool("on")
ConvCToBool("yes")
ConvCToBool(0)
ConvCToBool(False)
ConvCToBool("n")


@attrs.define
class DecoratorConverter:
    x: int = attrs.field()

    @x.converter
    def _to_int(self, field: attrs.Attribute, val: str | float) -> int:
        return int(val)


DecoratorConverter("foo")


# Validators
@attrs.define
class Validated:
    a: list[C] = attrs.field(
        validator=attrs.validators.deep_iterable(
            attrs.validators.instance_of(C), attrs.validators.instance_of(list)
        ),
    )
    a2: tuple[C] = attrs.field(
        validator=attrs.validators.deep_iterable(
            attrs.validators.instance_of(C),
            attrs.validators.instance_of(tuple),
        ),
    )
    a3: tuple[C] = attrs.field(
        validator=attrs.validators.deep_iterable(
            [attrs.validators.instance_of(C)],
            [attrs.validators.instance_of(tuple)],
        ),
    )
    b: list[C] = attrs.field(
        validator=attrs.validators.deep_iterable(
            attrs.validators.instance_of(C)
        ),
    )
    c: dict[C, D] = attrs.field(
        validator=attrs.validators.deep_mapping(
            attrs.validators.instance_of(C),
            attrs.validators.instance_of(D),
            attrs.validators.instance_of(dict),
        ),
    )
    d: dict[C, D] = attrs.field(
        validator=attrs.validators.deep_mapping(
            attrs.validators.instance_of(C), attrs.validators.instance_of(D)
        ),
    )
    d2: dict[C, D] = attrs.field(
        validator=attrs.validators.deep_mapping(
            attrs.validators.instance_of(C)
        ),
    )
    d3: dict[C, D] = attrs.field(
        validator=attrs.validators.deep_mapping(
            value_validator=attrs.validators.instance_of(C)
        ),
    )
    d4: dict[C, D] = attrs.field(
        validator=attrs.validators.deep_mapping(
            key_validator=[attrs.validators.instance_of(C)],
            value_validator=[attrs.validators.instance_of(C)],
            mapping_validator=[attrs.validators.instance_of(dict)],
        ),
    )
    e: str = attrs.field(
        validator=attrs.validators.matches_re(re.compile(r"foo"))
    )
    f: str = attrs.field(
        validator=attrs.validators.matches_re(r"foo", flags=42, func=re.search)
    )

    # Test different forms of instance_of
    g: int = attrs.field(validator=attrs.validators.instance_of(int))
    h: int = attrs.field(validator=attrs.validators.instance_of((int,)))
    j: int | str = attrs.field(
        validator=attrs.validators.instance_of((int, str))
    )
    k: int | str | C = attrs.field(
        validator=attrs.validators.instance_of((int, C, str))
    )
    kk: int | str | C = attrs.field(
        validator=attrs.validators.instance_of(int | C | str)
    )

    l: Any = attrs.field(
        validator=attrs.validators.not_(attrs.validators.in_("abc"))
    )
    m: Any = attrs.field(
        validator=attrs.validators.not_(
            attrs.validators.in_("abc"), exc_types=ValueError
        )
    )
    n: Any = attrs.field(
        validator=attrs.validators.not_(
            attrs.validators.in_("abc"), exc_types=(ValueError,)
        )
    )
    o: Any = attrs.field(
        validator=attrs.validators.not_(
            attrs.validators.in_("abc"), msg="spam"
        )
    )
    p: Any = attrs.field(
        validator=attrs.validators.not_(attrs.validators.in_("abc"), msg=None)
    )
    q: Any = attrs.field(
        validator=attrs.validators.optional(attrs.validators.instance_of(C))
    )
    r: Any = attrs.field(
        validator=attrs.validators.optional([attrs.validators.instance_of(C)])
    )
    s: Any = attrs.field(
        validator=attrs.validators.optional((attrs.validators.instance_of(C),))
    )


@attrs.define
class Validated2:
    num: int = attrs.field(validator=attrs.validators.ge(0))


with attrs.validators.disabled():
    Validated2(num=-1)


try:
    attrs.validators.set_disabled(True)
    Validated2(num=-1)
finally:
    attrs.validators.set_disabled(False)


# Custom repr()
@attrs.define
class WithCustomRepr:
    a: int = attrs.field(repr=True)
    b: str = attrs.field(repr=False)
    c: str = attrs.field(repr=lambda value: "c is for cookie")
    d: bool = attrs.field(repr=str)


# Check some of our own types
@attrs.define(eq=True, order=False)
class OrderFlags:
    a: int = attrs.field(eq=False, order=False)
    b: int = attrs.field(eq=True, order=True)


# on_setattr hooks
@attrs.define(on_setattr=attrs.setters.validate)
class ValidatedSetter:
    a: int
    b: str = attrs.field(on_setattr=attrs.setters.NO_OP)
    c: bool = attrs.field(on_setattr=attrs.setters.frozen)
    d: int = attrs.field(
        converter=int,
        on_setattr=[attrs.setters.convert, attrs.setters.validate],
    )
    e: bool = attrs.field(
        converter=attrs.converters.to_bool,
        on_setattr=attrs.setters.pipe(
            attrs.setters.convert, attrs.setters.validate
        ),
    )


vs = ValidatedSetter(1, "2", True, 4, False)
vs.d = "2"
vs.e = "yes"
vs.e = "foo"  # XXX: should only allow the literals we know


# field_transformer
def ft_hook(
    cls: type, attribs: list[attrs.Attribute]
) -> list[attrs.Attribute]:
    return attribs


@attrs.define(field_transformer=ft_hook)
class TransformedAttrs:
    x: int


# Auto-detect
@attrs.define(auto_detect=True)
class AutoDetect:
    x: int

    def __init__(self, x: int):
        self.x = x


@attrs.define(order=True)
class NGClass:
    x: int = attrs.field(default=42)


ngc = NGClass(1)


@attrs.frozen(str=True)
class NGFrozen:
    x: int


attrs.fields(NGFrozen).x.evolve(eq=False)
a = attrs.fields(NGFrozen).x
a.evolve(repr=False)


@attrs.define
class FactoryTest:
    a: list[int] = attrs.field(default=attrs.Factory(list))
    b: list[Any] = attrs.field(default=attrs.Factory(list, False))
    c: list[int] = attrs.field(default=attrs.Factory((lambda s: s.a), True))


attrs.asdict(FactoryTest(), tuple_keys=True)


# Check match_args stub
@attrs.define(match_args=False)
class MatchArgs:
    a: int = attrs.field()
    b: int = attrs.field()


attrs.asdict(FactoryTest())
attrs.asdict(FactoryTest(), retain_collection_types=False)


foo = object
if attrs.has(foo) or attrs.has(foo):
    foo.__attrs_attrs__


@attrs.define(unsafe_hash=True)
class Hashable:
    pass


def test(cls: type) -> None:
    if attrs.has(cls):
        attrs.resolve_types(cls)
