"""
Commonly useful hooks.
"""

from __future__ import absolute_import, division, print_function

import sys

from datetime import datetime
from enum import Enum

from ._compat import get_args, get_origin
from .converters import (
    to_attrs,
    to_dt,
    to_iterable,
    to_mapping,
    to_tuple,
    to_union,
)


if sys.version_info[:2] >= (3, 6):
    from typing import Union, get_type_hints
else:
    get_type_hints = None


__all__ = [
    "auto_convert",
    "auto_serialize",
    "make_auto_converter",
]


def make_auto_converter(converters):
    """
    Return a

    """
    if get_type_hints is None:
        raise RuntimeError("This function only works from Python 3.6 upwards")

    def auto_convert(cls, attribs):
        """
        A field transformer that tries to convert all attribs of a class to their
        annotated type.
        """
        # We cannot use attrs.resolve_types() here,
        # because "cls" is not yet a finished attrs class:
        type_hints = get_type_hints(cls)
        results = []
        for attrib in attribs:
            # Do not override explicitly defined converters!
            if attrib.converter is None:
                converter = _get_converter(type_hints[attrib.name], converters)
                attrib = attrib.assoc(converter=converter)
            results.append(attrib)

        return results

    return auto_convert


def _get_converter(
    type_,
    converters,
    iterable_types=frozenset({list, set, frozenset}),
    tuple_types=frozenset({tuple}),
    mapping_types=frozenset({dict}),
):
    """
    Recursively resolves concrete and generic types and return a proper converter.
    """
    # Detect whether "type_" is a container type.  Currently we need
    # to check, e.g., for "typing.List".  From python 3.9, we also
    # need to check for "list" directly.
    origin = get_origin(type_)
    if origin is None:
        # Get converter for concrete type
        if getattr(type_, "__attrs_attrs__", None) is not None:
            # Attrs classes
            converter = to_attrs(type_)
        else:
            # Check if type is in converters dict
            for convert_type, convert_func in converters.items():
                if issubclass(type_, convert_type):
                    converter = convert_func
                    break
            else:
                # Fall back to simple types like bool, int, float, str, Enum, ...
                converter = type_
    else:
        # Get converter for generic type
        args = get_args(type_)
        if origin in iterable_types:
            item_converter = _get_converter(args[0], converters)
            converter = to_iterable(origin, item_converter)
        elif origin in tuple_types:
            if len(args) == 2 and args[1] == ...:
                # "frozen list" variant of tuple
                item_converter = _get_converter(args[0], converters)
                converter = to_iterable(tuple, item_converter)
            else:
                # "struct" variant of tuple
                item_converters = [_get_converter(t, converters) for t in args]
                converter = to_tuple(tuple, item_converters)
        elif origin in mapping_types:
            key_converter = _get_converter(args[0], converters)
            val_converter = _get_converter(args[1], converters)
            converter = to_mapping(dict, key_converter, val_converter)
        elif origin is Union:
            item_converters = [_get_converter(t, converters) for t in args]
            converter = to_union(item_converters)
        else:
            raise TypeError(
                f"Cannot create converter for generic type: {type_}"
            )

    return converter


auto_convert = make_auto_converter({datetime: to_dt})
"""Auto-convert :class:`datetime.datetime` as well as other stuff."""


def auto_serialize(inst, attrib, value):
    """Inverse hook to :func:`auto_convert` for use with
    :func:`attrs.asdict()`.
    """
    if isinstance(value, datetime):
        return datetime.isoformat(value)
    if isinstance(value, Enum):
        return value.value
    return value
