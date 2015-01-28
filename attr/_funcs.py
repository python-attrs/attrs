# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


def ls(cl):
    """
    Returns the list of ``attrs`` attributes for a class.

    :param cl: Class to introspect.
    :type cl: type

    :raise TypeError: If *cl* is not a class.
    :raise ValueError: If *cl* is not an ``attrs`` class.

    :rtype: :class:`list` of :class:`attr.Attribute`
    """
    if not isinstance(cl, type):
        raise TypeError("Passed object must be a class.")
    attrs = getattr(cl, "__attrs_attrs__", None)
    if attrs is None:
        raise ValueError("{cl!r} is not an attrs-decorated class.".format(
            cl=cl
        ))
    return attrs


def to_dict(inst, recurse=True):
    """
    Return the ``attrs`` attribute values of *i* as a dict.  Optionally recurse
    into other ``attrs``-decorated classes.

    :param inst: Instance of a ``attrs``-decorated class.

    :param recurse: Recurse into classes that are also ``attrs``-decorated.
    :type recurse: bool

    :rtype: :class:`dict`
    """
    attrs = ls(inst.__class__)
    rv = {}
    for a in attrs:
        v = getattr(inst, a.name)
        if recurse is True and has(v.__class__):
            rv[a.name] = to_dict(v, recurse=True)
        else:
            rv[a.name] = v
    return rv


def has(cl):
    """
    Check whether *cl* is a class with ``attrs`` attributes.

    :param cl: Class to introspect.
    :type cl: type

    :raise TypeError: If *cl* is not a class.

    :rtype: :class:`bool`
    """
    try:
        ls(cl)
    except ValueError:
        return False
    else:
        return True
