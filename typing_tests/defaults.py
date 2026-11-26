# SPDX-License-Identifier: MIT

"""
Decorator-based defaults (@x.default).
"""

from __future__ import annotations

import attr
import attrs


@attrs.define
class DecoratorDefault:
    x: int = attrs.field()

    @x.default
    def _x_default(self) -> int:
        return 42


DecoratorDefault()
DecoratorDefault(1)


@attrs.define
class DecoratorDefaultAfterDefault:
    x: int = 1
    y: int = attrs.field()

    @y.default
    def _y_default(self) -> int:
        return self.x + 1


DecoratorDefaultAfterDefault()
DecoratorDefaultAfterDefault(1, 2)


# Classic API --


@attr.s
class ClassicDecoratorDefault:
    x: int = attr.ib()

    @x.default
    def _x_default(self) -> int:
        return 42


ClassicDecoratorDefault()
ClassicDecoratorDefault(1)
