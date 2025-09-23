# SPDX-License-Identifier: MIT

from __future__ import annotations

import enum

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, NamedTuple

from .exceptions import NotAnAttrsClassError


if TYPE_CHECKING:
    from ._make import Attribute


class ClassProps(NamedTuple):
    """
    Effective class properties as derived from parameters to attr.s() or
    define() decorators.

    .. versionadded:: 25.4.0
    """

    class Hashability(enum.Enum):
        """
        The hashability of a class.

        .. versionadded:: 25.4.0
        """

        HASHABLE = "hashable"
        """Write a ``__hash__``."""
        HASHABLE_CACHED = "hashable_cache"
        """Write a ``__hash__`` and cache the hash."""
        UNHASHABLE = "unhashable"
        """Set ``__hash__`` to ``None``."""
        LEAVE_ALONE = "leave_alone"
        """Don't touch ``__hash__``."""

    class KeywordOnly(enum.Enum):
        """
        How attributes should be treated regarding keyword-only parameters.

        .. versionadded:: 25.4.0
        """

        NO = "no"
        """Attributes are not keyword-only."""
        YES = "yes"
        """Attributes in current class without kw_only=False are keyword-only."""
        FORCE = "force"
        """All attributes are keyword-only."""

    is_exception: bool
    is_slotted: bool
    has_weakref_slot: bool
    is_frozen: bool
    kw_only: ClassProps.KeywordOnly
    collect_by_mro: bool
    init: bool
    repr: bool
    eq: bool
    order: bool
    hash: ClassProps.Hashability
    match_args: bool
    str: bool
    getstate_setstate: bool
    on_setattr: Callable[[str, Any], Any]
    field_transformer: Callable[[Attribute], Attribute]

    @property
    def is_hashable(self):
        return (
            self.hash is ClassProps.Hashability.HASHABLE
            or self.hash is ClassProps.Hashability.HASHABLE_CACHED
        )


def inspect(cls: type) -> ClassProps:
    """
    Inspect the class and return it's effective build parameters.

    Args:
        cls: The class to inspect.

    Returns:
        The effective build parameters of the class.

    Raises:
        NotAnAttrsClassError: If the class is not an *attrs*-decorated class.

    .. versionadded:: 25.4.0
    """
    try:
        return cls.__dict__["__attrs_props__"]
    except IndexError:
        msg = f"{cls!r} is not an attrs-decorated class."
        raise NotAnAttrsClassError(msg) from None
