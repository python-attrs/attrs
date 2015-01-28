# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


from ._dunders import (
    NOTHING,
    _add_cmp,
    _add_hash,
    _add_init,
    _add_repr,
)


class Attribute(object):
    """
    *Read-only* representation of an attribute.

    :attribute name: The name of the attribute.
    :attribute default_value: A value that is used if an ``attrs``-generated
        ``__init__`` is used and no value is passed while instantiating.
    :attribute default_factory: A :func:`callable` that is called to obtain
        a default value if an ``attrs``-generated ``__init__`` is used and no
        value is passed while instantiating.
    """
    def __init__(self, name, default_value, default_factory):
        self.name = name
        self.default_value = default_value
        self.default_factory = default_factory

    @classmethod
    def from_counting_attr(cl, name, ca):
        return cl(
            name=name,
            default_value=ca.default_value,
            default_factory=ca.default_factory,
        )


_a = [Attribute(name=name, default_value=NOTHING, default_factory=NOTHING)
      for name in ("name", "default_value", "default_factory",)]
Attribute = _add_cmp(_add_repr(Attribute, attrs=_a), attrs=_a)


class _CountingAttr(object):
    __attrs_attrs__ = [
        Attribute(name=name, default_value=NOTHING, default_factory=NOTHING)
        for name
        in ("counter", "default_value", "default_factory",)
    ]
    counter = 0

    def __init__(self, default_value=NOTHING, default_factory=NOTHING):
        _CountingAttr.counter += 1
        self.counter = _CountingAttr.counter
        self.default_value = default_value
        self.default_factory = default_factory


_CountingAttr = _add_cmp(_add_repr(_CountingAttr))


def _make_attr(default_value=NOTHING, default_factory=NOTHING):
    """
    Create a new attribute on a class.

    Does nothing unless the class is also decorated with :func:`attr.s`!
    """
    if default_value is not NOTHING and default_factory is not NOTHING:
        raise ValueError(
            "Specifying both default_value and default_factory is "
            "ambiguous."
        )

    return _CountingAttr(
        default_value=default_value,
        default_factory=default_factory,
    )


def _get_attrs(cl):
    """
    Return list of tuples of `(name, _Attr)`.
    """
    attrs = []

    for name, instance in sorted((
            (n, i) for n, i in cl.__dict__.items()
            if isinstance(i, _CountingAttr)
    ), key=lambda e: e[1].counter):
        attrs.append((name, instance))

    return attrs


def _add_methods(maybe_cl=None, add_repr=True, add_cmp=True, add_hash=True,
                 add_init=True):
    """
    A class decorator that adds `dunder
    <https://wiki.python.org/moin/DunderAlias>`_\ -methods according to the
    specified attributes using :func:`attr.ib`.

    :param add_repr: Create a ``__repr__`` method with a human readable
        represantation of ``attrs`` attributes..
    :type add_repr: bool

    :param add_cmp: Create ``__eq__``, ``__ne__``, ``__lt__``, ``__le__``,
        ``__gt__``, and ``__ge__`` methods that compare the class as if it were
        a tuple of its ``attrs`` attributes.
    :type add_cmp: bool

    :param add_hash: Add a ``__hash__`` method that returns the :func:`hash` of
    a tuple of all ``attrs`` attribute values.
    :type add_hash: bool

    :param add_init: Add a ``__init__`` method that initialiazes the ``attrs``
        attributes.
    :type add_init: bool
    """
    # attrs_or class type depends on the usage of the decorator.  It's a class
    # if it's used as `@_add_methods` but ``None`` (or a value passed) if used
    # as `@_add_methods()`.
    if isinstance(maybe_cl, type):
        cl = maybe_cl
        cl.__attrs_attrs__ = [
            Attribute.from_counting_attr(name=name, ca=ca)
            for name, ca in _get_attrs(cl)
        ]
        return _add_init(_add_hash(_add_cmp(_add_repr(cl))))
    else:
        def wrap(cl):
            cl.__attrs_attrs__ = [
                Attribute.from_counting_attr(name=name, ca=ca)
                for name, ca in _get_attrs(cl)
            ]
            if add_repr is True:
                cl = _add_repr(cl)
            if add_cmp is True:
                cl = _add_cmp(cl)
            if add_hash is True:
                cl = _add_hash(cl)
            if add_init is True:
                cl = _add_init(cl)
            return cl

        return wrap
