import re

from typing import Any, Dict, List, Tuple, Union

import attr


# Typing via "type" Argument ---


@attr.s
class C:
    a = attr.ib(type=int)


c = C(1)
C(a=1)


@attr.s
class D:
    x = attr.ib(type=List[int])


@attr.s
class E:
    y = attr.ib(type="List[int]")


@attr.s
class F:
    z = attr.ib(type=Any)


# Typing via Annotations ---


@attr.s
class CC:
    a: int = attr.ib()


cc = CC(1)
CC(a=1)


@attr.s
class DD:
    x: List[int] = attr.ib()


@attr.s
class EE:
    y: "List[int]" = attr.ib()


@attr.s
class FF:
    z: Any = attr.ib()


# Inheritance --


@attr.s
class GG(DD):
    y: str = attr.ib()


GG(x=[1], y="foo")


@attr.s
class HH(DD, EE):
    z: float = attr.ib()


HH(x=[1], y=[], z=1.1)


# same class
c == cc


# Exceptions
@attr.s(auto_exc=True)
class Error(Exception):
    x = attr.ib()


try:
    raise Error(1)
except Error as e:
    e.x
    e.args
    str(e)


# Converters
# XXX: Currently converters can only be functions so none of this works
# although the stubs should be correct.

# @attr.s
# class ConvCOptional:
#     x: Optional[int] = attr.ib(converter=attr.converters.optional(int))


# ConvCOptional(1)
# ConvCOptional(None)


# @attr.s
# class ConvCDefaultIfNone:
#     x: int = attr.ib(converter=attr.converters.default_if_none(42))


# ConvCDefaultIfNone(1)
# ConvCDefaultIfNone(None)


# Validators
@attr.s
class Validated:
    a = attr.ib(
        type=List[C],
        validator=attr.validators.deep_iterable(
            attr.validators.instance_of(C), attr.validators.instance_of(list)
        ),
    )
    a = attr.ib(
        type=Tuple[C],
        validator=attr.validators.deep_iterable(
            attr.validators.instance_of(C), attr.validators.instance_of(tuple)
        ),
    )
    b = attr.ib(
        type=List[C],
        validator=attr.validators.deep_iterable(
            attr.validators.instance_of(C)
        ),
    )
    c = attr.ib(
        type=Dict[C, D],
        validator=attr.validators.deep_mapping(
            attr.validators.instance_of(C),
            attr.validators.instance_of(D),
            attr.validators.instance_of(dict),
        ),
    )
    d = attr.ib(
        type=Dict[C, D],
        validator=attr.validators.deep_mapping(
            attr.validators.instance_of(C), attr.validators.instance_of(D)
        ),
    )
    e = attr.ib(validator=attr.validators.matches_re(r"foo"))
    f = attr.ib(
        validator=attr.validators.matches_re(r"foo", flags=42, func=re.search)
    )

    # Test different forms of instance_of
    g: int = attr.ib(validator=attr.validators.instance_of(int))
    h: int = attr.ib(validator=attr.validators.instance_of((int,)))
    j: Union[int, str] = attr.ib(
        validator=attr.validators.instance_of((int, str))
    )
    k: Union[int, str, C] = attr.ib(
        validator=attr.validators.instance_of((int, C, str))
    )


# Custom repr()
@attr.s
class WithCustomRepr:
    a = attr.ib(repr=True)
    b = attr.ib(repr=False)
    c = attr.ib(repr=lambda value: "c is for cookie")
    d = attr.ib(repr=str)


# Check some of our own types
@attr.s(eq=True, order=False)
class OrderFlags:
    a = attr.ib(eq=False, order=False)
    b = attr.ib(eq=True, order=True)


# on_setattr hooks
@attr.s(on_setattr=attr.setters.validate)
class ValidatedSetter:
    a = attr.ib()
    b = attr.ib(on_setattr=attr.setters.NO_OP)
    c = attr.ib(on_setattr=attr.setters.frozen)
    d = attr.ib(on_setattr=[attr.setters.convert, attr.setters.validate])
    d = attr.ib(
        on_setattr=attr.setters.pipe(
            attr.setters.convert, attr.setters.validate
        )
    )


# Auto-detect
# XXX: needs support in mypy
# @attr.s(auto_detect=True)
# class AutoDetect:
#     x: int

#     def __init__(self, x: int):
#         self.x = x

# Provisional APIs
@attr.define(order=True)
class NGClass:
    x: int = attr.field(default=42)


# XXX: needs support in mypy
# ngc = NGClass(1)


@attr.mutable(slots=False)
class NGClass2:
    x: int


# XXX: needs support in mypy
# ngc2 = NGClass2(1)


@attr.frozen(str=True)
class NGFrozen:
    x: int


# XXX: needs support in mypy
# ngf = NGFrozen(1)
