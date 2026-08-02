# SPDX-License-Identifier: MIT

"""
Classes Without Boilerplate
"""

import sys

from functools import partial
from typing import Callable, Literal, Protocol

from . import exceptions, setters
from ._config import get_run_validators, set_run_validators
from ._funcs import asdict, assoc, astuple, has, resolve_types
from ._make import (
    NOTHING,
    Attribute,
    Converter,
    Factory,
    _Nothing,
    attrib,
    attrs,
    evolve,
    fields,
    fields_dict,
    make_class,
    validate,
)
from ._next_gen import define, field, frozen, mutable


s = attributes = attrs
ib = attr = attrib
dataclass = partial(attrs, auto_attribs=True)  # happy Easter ;)


class AttrsInstance(Protocol):
    pass


NothingType = Literal[_Nothing.NOTHING]

__all__ = [
    "NOTHING",
    "Attribute",
    "AttrsInstance",
    "Converter",
    "Factory",
    "NothingType",
    "asdict",
    "assoc",
    "astuple",
    "attr",
    "attrib",
    "attributes",
    "attrs",
    "cmp_using",
    "converters",
    "define",
    "evolve",
    "exceptions",
    "field",
    "fields",
    "fields_dict",
    "filters",
    "frozen",
    "get_run_validators",
    "has",
    "ib",
    "make_class",
    "mutable",
    "resolve_types",
    "s",
    "set_run_validators",
    "setters",
    "validate",
    "validators",
]


def _make_getattr(mod_name: str) -> Callable:
    """
    Create a metadata proxy for packaging information that uses *mod_name* in
    its warnings and errors.
    """
    _LAZY_SUBMODULES = {"converters", "validators", "filters"}

    def __getattr__(name: str) -> str:
        if name in _LAZY_SUBMODULES:
            import importlib

            mod = importlib.import_module(f".{name}", mod_name)
            sys.modules[mod_name].__dict__[name] = mod
            return mod

        if name == "VersionInfo":
            from ._version_info import VersionInfo

            globals()[name] = VersionInfo

            return VersionInfo

        if name == "cmp_using":
            from ._cmp import cmp_using

            globals()[name] = cmp_using

            return cmp_using

        if name not in ("__version__", "__version_info__"):
            msg = f"module {mod_name} has no attribute {name}"
            raise AttributeError(msg)

        from importlib.metadata import metadata

        meta = metadata("attrs")

        if name == "__version_info__":
            from ._version_info import VersionInfo

            return VersionInfo._from_version_string(meta["version"])

        return meta["version"]

    return __getattr__


__getattr__ = _make_getattr(__name__)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
