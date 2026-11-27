# SPDX-License-Identifier: MIT

"""
Typing examples that rely on Mypy-specific features (mostly the attrs plugin).
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

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


@attr.s
class CC:
    a: int = attr.ib()


cc = CC(1)


# same class
c == cc


# Validators
@attr.s
class Validated:
    a = attr.ib(
        type=List[C],
        validator=attr.validators.deep_iterable(
            attr.validators.instance_of(C), attr.validators.instance_of(list)
        ),
    )
    a2 = attr.ib(
        type=Tuple[C],
        validator=attr.validators.deep_iterable(
            attr.validators.instance_of(C), attr.validators.instance_of(tuple)
        ),
    )
    a3 = attr.ib(
        type=Tuple[C],
        validator=attr.validators.deep_iterable(
            [attr.validators.instance_of(C)],
            [attr.validators.instance_of(tuple)],
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
    d2 = attr.ib(
        type=Dict[C, D],
        validator=attr.validators.deep_mapping(attr.validators.instance_of(C)),
    )
    d3 = attr.ib(
        type=Dict[C, D],
        validator=attr.validators.deep_mapping(
            value_validator=attr.validators.instance_of(C)
        ),
    )
    d4 = attr.ib(
        type=Dict[C, D],
        validator=attr.validators.deep_mapping(
            key_validator=[attr.validators.instance_of(C)],
            value_validator=[attr.validators.instance_of(C)],
            mapping_validator=[attr.validators.instance_of(dict)],
        ),
    )
