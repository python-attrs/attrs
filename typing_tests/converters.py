# SPDX-License-Identifier: MIT
# pyright: strict

"""
Converter features.

Features that a type checker doesn't support are silenced using that type
checker's own ignore comments.
"""

from __future__ import annotations

from typing import Any

import attr
import attrs


@attrs.define
class ConvCOptional:
    x: int | None = attrs.field(converter=attrs.converters.optional(int))


ConvCOptional(1)
ConvCOptional(None)


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


# Mypy only supports named functions, types, and lambdas as converters:
# https://github.com/python/mypy/issues/15736


@attrs.define
class ConvCPipe:
    x: str = attrs.field(converter=attrs.converters.pipe(int, str))  # type: ignore[misc]


ConvCPipe(3.4)
ConvCPipe("09")


@attrs.define
class ConvCDefaultIfNone:
    x: int = attrs.field(converter=attrs.converters.default_if_none(42))  # type: ignore[misc]


ConvCDefaultIfNone(1)
ConvCDefaultIfNone(None)


# Only Pyrefly supports decorator-based converters.
@attrs.define
class DecoratorConverter:
    x: int = attrs.field()

    @x.converter  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUntypedFunctionDecorator]  # ty: ignore[missing-attribute]
    def _to_int(self, field: attrs.Attribute[Any], val: str | float) -> int:
        return int(val)


DecoratorConverter("foo")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # ty: ignore[invalid-argument-type]


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

# Mypy doesn't apply converters to assignments.
vs.d = "2"  # type: ignore[assignment]
vs.e = "yes"  # type: ignore[assignment]
vs.e = "foo"  # type: ignore[assignment]  # XXX: should only allow the literals we know


# Classic API --


@attr.s
class ClassicConvCOptional:
    x: int | None = attr.ib(converter=attr.converters.optional(int))


ClassicConvCOptional(1)
ClassicConvCOptional(None)


@attr.s
class ClassicConvCToBool:
    x: int = attr.ib(converter=attr.converters.to_bool)


ClassicConvCToBool(1)
ClassicConvCToBool(True)
ClassicConvCToBool("on")
ClassicConvCToBool("yes")
ClassicConvCToBool(0)
ClassicConvCToBool(False)
ClassicConvCToBool("n")
