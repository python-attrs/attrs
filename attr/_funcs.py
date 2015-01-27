# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


def ls(cl):
    """
    Returns the list of `Attribute`s for a class or an instance.
    """
    if not isinstance(cl, type):
        cl = cl.__class__
    attrs = getattr(cl, "__attrs_attrs__", None)
    if attrs is None:
        raise TypeError("{cl!r} is not an attrs-decorated class.".format(
            cl=cl
        ))
    return attrs


def to_dict(i, recurse=True):
    """
    Return the values of *i* as a dict.  Optionally recurse into classes that
    are also decorated with attrs.
    """
    attrs = ls(i)
    rv = {}
    for a in attrs:
        v = getattr(i, a.name)
        if recurse is True and getattr(v, "__attrs_attrs__", None) is not None:
            rv[a.name] = to_dict(v, recurse=True)
        else:
            rv[a.name] = v
    return rv
