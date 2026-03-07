# SPDX-License-Identifier: MIT
"""A Sphinx extension to document cached properties on slots classes

Add ``"attrs.sphinx_cached_property"`` to the ``extensions`` list in Sphinx's
conf.py to use this. Otherwise, cached properties of ``@define(slots=True)``
classes will be inaccessible.

"""
from functools import cached_property
from typing import Any

from sphinx.application import Sphinx

from . import __version__


def get_cached_property_for_member_descriptor(
    cls: type, name: str, default=None
) -> cached_property | Any:
    """If the attribute is for a cached property, return the ``cached_property``

    Otherwise, delegate to normal ``getattr``

    """
    props = getattr(cls, "__attrs_cached_properties__", None)
    if props is None or name not in props:
        return getattr(cls, name, default)
    return props[name]


def setup(app: Sphinx) -> dict[str, str | bool]:
    """Install the special attribute getter for cached properties of slotted classes"""
    app.add_autodoc_attrgetter(
        object, get_cached_property_for_member_descriptor
    )
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
