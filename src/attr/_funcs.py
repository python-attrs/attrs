from __future__ import absolute_import, division, print_function

import copy

from ._compat import iteritems
from ._make import Attribute, NOTHING, fields


def asdict(inst, recurse=True, filter=None, dict_factory=dict):
    """
    Return the ``attrs`` attribute values of *i* as a dict.  Optionally recurse
    into other ``attrs``-decorated classes.

    :param inst: Instance of a ``attrs``-decorated class.

    :param bool recurse: Recurse into classes that are also
        ``attrs``-decorated.

    :param callable filter: A callable whose return code deteremines whether an
        attribute or element is included (``True``) or dropped (``False``).  Is
        called with the :class:`attr.Attribute` as the first argument and the
        value as the second argument.

    :param callable dict_factory: A callable to produce dictionaries from. For
        example, to produce ordered dictionaries instead of normal Python
        dictionaries, pass in ``collections.OrderedDict``.

    :rtype: :class:`dict`

    .. versionadded:: 16.0.0
        *dict_factory*
    """
    attrs = fields(inst.__class__)
    rv = dict_factory()
    for a in attrs:
        v = getattr(inst, a.name)
        if filter is not None and not filter(a, v):
            continue
        if recurse is True:
            if has(v.__class__):
                rv[a.name] = asdict(v, recurse=True, filter=filter)
            elif isinstance(v, (tuple, list, set)):
                rv[a.name] = [
                    asdict(i, recurse=True, filter=filter)
                    if has(i.__class__) else i
                    for i in v
                ]
            elif isinstance(v, dict):
                rv[a.name] = dict((asdict(kk) if has(kk.__class__) else kk,
                                   asdict(vv) if has(vv.__class__) else vv)
                                  for kk, vv in iteritems(v))
            else:
                rv[a.name] = v
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
