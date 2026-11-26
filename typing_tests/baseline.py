# SPDX-License-Identifier: MIT
# pyright: strict

"""
Baseline features that should be supported by all type checkers.
"""

from __future__ import annotations

import copy
import re
import sys

from typing import Any, Generator

import attrs


@attrs.define(order=True)
class NGClass:
    x: int = attrs.field(default=42)


ngc = NGClass(1)

ngc = attrs.assoc(ngc, x=1)
ngc = attrs.evolve(ngc, x=1)


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
C(a=1)
c.a

if sys.version_info >= (3, 13):
    # Mypy's attrs plugin doesn't add __replace__.
    c = copy.replace(c, a=1)  # type: ignore[arg-type]


@attrs.frozen
class D:
    a: int


D(1).a


@attrs.define
class D2:
    x: list[int] = attrs.field()


li: list[int] = D2([1]).x


@attrs.define
class E:
    y: "list[int]" = attrs.field()


li = E([1]).y


@attrs.define
class F:
    z: Any = attrs.field()


@attrs.define
class Derived(C):
    b: int


Derived(1, 2).a
Derived(1, 2).b


@attrs.define
class GG(D2):
    y: str = attrs.field()


GG(x=[1], y="foo")


@attrs.define(slots=False)
class Base1:
    x: list[int]


@attrs.define(slots=False)
class Base2:
    y: "list[int]"


@attrs.define
class HH(Base1, Base2):
    z: float


HH(x=[1], y=[], z=1.1)


@attrs.define
class Error(Exception):
    x: int


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
except Error2 as e:
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
class ValidatedOptionalOverTuple:
    num: int | None = attrs.field(
        validator=attrs.validators.optional(
            (attrs.validators.instance_of(int), attrs.validators.ge(0))
        )
    )


@attrs.define
class ValidatedInconsistentOr:
    num: int | str = attrs.field(
        validator=attrs.validators.or_(
            # Various types of validators.
            attrs.validators.ge(0),
            attrs.validators.instance_of(str),
        )
    )


@attrs.define
class Validated2:
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


def gen_on_setattr_hook(
    instance: Any, attribute: attrs.Attribute[Any], new_value: Any
) -> Generator[int]:
    yield 42


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
    f: int = attrs.field(on_setattr=gen_on_setattr_hook)


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
attrs.asdict(FactoryTest(), tuple_keys=True)


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


@attrs.define(init=False)
class NoInit:
    x: int

    def __init__(self, s: str):
        self.x = int(s)


NoInit("42")


# Auto-detect is True by default
@attrs.define
class AutoDetect:
    x: int

    def __init__(self, s: str):
        self.x = int(s)


AutoDetect(s="42")  # type: ignore[call-arg]
