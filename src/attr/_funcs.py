from __future__ import absolute_import, division, print_function

import copy

from ._compat import iteritems
from ._make import Attribute, NOTHING, fields, _obj_setattr


def asdict(inst, recurse=True, filter=None, dict_factory=dict,
           retain_collection_types=False):
    """
    Return the ``attrs`` attribute values of *inst* as a dict.

    Optionally recurse into other ``attrs``-decorated classes.

    :param inst: Instance of an ``attrs``-decorated class.
    :param bool recurse: Recurse into classes that are also
        ``attrs``-decorated.
    :param callable filter: A callable whose return code deteremines whether an
        attribute or element is included (``True``) or dropped (``False``).  Is
        called with the :class:`attr.Attribute` as the first argument and the
        value as the second argument.
    :param callable dict_factory: A callable to produce dictionaries from.  For
        example, to produce ordered dictionaries instead of normal Python
        dictionaries, pass in ``collections.OrderedDict``.
    :param bool retain_collection_types: Do not convert to ``list`` when
        encountering an attribute which is type ``tuple`` or ``set``.  Only
        meaningful if ``recurse`` is ``True``.

    :rtype: return type of *dict_factory*

    ..  versionadded:: 16.0.0 *dict_factory*
    ..  versionadded:: 16.1.0 *retain_collection_types*
    """
    attrs = fields(inst.__class__)
    rv = dict_factory()
    for a in attrs:
        v = getattr(inst, a.name)
        if filter is not None and not filter(a, v):
            continue
        if recurse is True:
            if has(v.__class__):
                rv[a.name] = asdict(v, recurse=True, filter=filter,
                                    dict_factory=dict_factory)
            elif isinstance(v, (tuple, list, set)):
                cf = v.__class__ if retain_collection_types is True else list
                rv[a.name] = cf([
                    asdict(i, recurse=True, filter=filter,
                           dict_factory=dict_factory)
                    if has(i.__class__) else i
                    for i in v
                ])
            elif isinstance(v, dict):
                df = dict_factory
                rv[a.name] = df((
                    asdict(kk, dict_factory=df) if has(kk.__class__) else kk,
                    asdict(vv, dict_factory=df) if has(vv.__class__) else vv)
                    for kk, vv in iteritems(v))
            else:
                rv[a.name] = v
        else:
            rv[a.name] = v
    return rv


def has(cls):
    """
    Check whether *cls* is a class with ``attrs`` attributes.

    :param type cls: Class to introspect.

    :raise TypeError: If *cls* is not a class.

    :rtype: :class:`bool`
    """
    return getattr(cls, "__attrs_attrs__", None) is not None


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
        _obj_setattr(new, k, v)
    return new
