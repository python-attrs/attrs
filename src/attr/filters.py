# SPDX-License-Identifier: MIT

"""
Commonly useful filters for `attr.asdict`.
"""

from ._make import Attribute


def _split_what(what):
    """
    Returns a tuple of `frozenset`s of classes and attributes.
    """
    return (
        frozenset(cls for cls in what if isinstance(cls, type)),
        frozenset(cls for cls in what if isinstance(cls, str)),
        frozenset(cls for cls in what if isinstance(cls, Attribute)),
    )


def include(*what):
    """
    Include *what*.

    :param what: What to include.
    :type what: `list` of classes `type`, field names `str` or
        `attrs.Attribute`\\ s

    :rtype: `callable`

    .. versionchanged:: 22.3.0 Accept field name string as input argument
    """
    cls, names, attrs = _split_what(what)

    def include_(attribute, value):
        return (
            value.__class__ in cls
            or attribute.name in names
            or attribute in attrs
        )

    return include_


def exclude(*what):
    """
    Exclude *what*.

    :param what: What to exclude.
    :type what: `list` of classes `type`, field names `str` or
        `attrs.Attribute`\\ s.

    :rtype: `callable`

    .. versionchanged:: 22.3.0 Accept field name string as input argument
    """
    cls, names, attrs = _split_what(what)

    def exclude_(attribute, value):
        return not (
            value.__class__ in cls
            or attribute.name in names
            or attribute in attrs
        )

    return exclude_
