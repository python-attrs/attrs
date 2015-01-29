# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import copy

from ._compat import iteritems
from ._dunders import NOTHING
from ._make import Attribute


def fields(cl):
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
    return copy.deepcopy(attrs)


def asdict(inst, recurse=True):
    """
    Return the ``attrs`` attribute values of *i* as a dict.  Optionally recurse
    into other ``attrs``-decorated classes.

    :param inst: Instance of a ``attrs``-decorated class.

    :param recurse: Recurse into classes that are also ``attrs``-decorated.
    :type recurse: bool

    :rtype: :class:`dict`
    """
    attrs = fields(inst.__class__)
    rv = {}
    for a in attrs:
        v = getattr(inst, a.name)
        if recurse is True and has(v.__class__):
            rv[a.name] = asdict(v, recurse=True)
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
        fields(cl)
    except ValueError:
        return False
    else:
        return True


def assoc(inst, **changes):
    """
    Copy *inst* and apply *changes*.

    :param inst: Instance of a class with ``attrs`` attributes.

    :param changes: Keyword changes in the new copy.

    :return: A copy of inst with *changes* incorporated.
    """
    new = copy.copy(inst)
    for k, v in iteritems(changes):
        a = getattr(new.__class__, k, NOTHING)
        if a is NOTHING or not isinstance(a, Attribute):
            raise ValueError(
                "{k} is not an attrs attribute on {cl}."
                .format(k=k, cl=new.__class__)
            )
        setattr(new, k, v)
    return new
