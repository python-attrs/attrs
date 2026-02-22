# SPDX-License-Identifier: MIT
"""A Sphinx extension to document cached properties on slots classes

Add ``"attrs.sphinx_cached_property"`` to the ``extensions`` list in Sphinx's
conf.py to use this.

"""

from sphinx.application import Sphinx


def get_cached_property_for_member_descriptor(
    cls: type, name: str, default=None
):
    props = getattr(cls, "__attrs_cached_properties__", None)
    if props is None or name not in props:
        return getattr(cls, name, default)
    return props[name]


def setup(app: Sphinx):
    app.add_autodoc_attrgetter(
        object, get_cached_property_for_member_descriptor
    )
