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
    :attribute default_value: see :func:`attr.ib`
    :attribute factory: see :func:`attr.ib`
    :attribute validator: see :func:`attr.ib`
    """
    _attributes = [
        "name", "default_value", "factory", "validator",
    ]  # we can't use ``attrs`` so we have to cheat a little.

    def __init__(self, **kw):
        try:
            for a in Attribute._attributes:
                setattr(self, a, kw[a])
        except KeyError:
            raise TypeError("Missing argument '{arg}'.".format(arg=a))

    @classmethod
    def from_counting_attr(cl, name, ca):
        return cl(name=name,
                  **dict((k, getattr(ca, k))
                         for k
                         in Attribute._attributes
                         if k != "name"))


_a = [Attribute(name=name, default_value=NOTHING, factory=NOTHING,
                validator=None)
      for name in Attribute._attributes]
Attribute = _add_hash(
    _add_cmp(_add_repr(Attribute, attrs=_a), attrs=_a), attrs=_a
)


class _CountingAttr(object):
    __attrs_attrs__ = [
        Attribute(name=name, default_value=NOTHING, factory=NOTHING,
                  validator=None)
        for name
        in ("counter", "default_value", "factory",)
    ]
    counter = 0

    def __init__(self, default_value, factory, validator):
        _CountingAttr.counter += 1
        self.counter = _CountingAttr.counter
        self.default_value = default_value
        self.factory = factory
        self.validator = validator


_CountingAttr = _add_cmp(_add_repr(_CountingAttr))


def attr(default_value=NOTHING, factory=NOTHING, validator=None):
    """
    Create a new attribute on a class.

    .. warning::

        Does nothing unless the class is also decorated with :func:`attr.s`!

    :param default_value: Value that is used if an ``attrs``-generated
        ``__init__`` is used and no value is passed while instantiating.
    :type default_value: Any value.

    :param factory: :func:`callable` that is called to obtain
        a default value if an ``attrs``-generated ``__init__`` is used and no
        value is passed while instantiating.
    :type factory: callable

    :param validator: :func:`callable` that is called within
        ``attrs``-generated ``__init__`` methods with the :class:`Attribute` as
        the first parameter and the passed value as the second parameter.

        The return value is *not* inspected so the validator has to throw an
        exception itself.
    :type validator: callable
    """
    if default_value is not NOTHING and factory is not NOTHING:
        raise ValueError(
            "Specifying both default_value and factory is "
            "ambiguous."
        )

    return _CountingAttr(
        default_value=default_value,
        factory=factory,
        validator=validator,
    )


def _transform_attrs(cl):
    """
    Transforms all `_CountingAttr`s on a class into `Attribute`s and saves the
    list in `__attrs_attrs__`.
    """
    cl.__attrs_attrs__ = []
    had_default = False
    for attr_name, ca in sorted(
            ((name, attr) for name, attr
             in cl.__dict__.items()
             if isinstance(attr, _CountingAttr)),
            key=lambda e: e[1].counter
    ):
        a = Attribute.from_counting_attr(name=attr_name, ca=ca)
        if had_default is True and \
                a.default_value is a.factory is NOTHING:
            raise ValueError(
                "No mandatory attributes allowed after an atribute with a "
                "default value or factory.  Attribute in question: {a!r}"
                .format(a=a)
            )
        elif had_default is False and (a.default_value is not NOTHING
                                       or a.factory is not NOTHING):
            had_default = True
        cl.__attrs_attrs__.append(a)
        setattr(cl, attr_name, a)


def attributes(maybe_cl=None, add_repr=True, add_cmp=True, add_hash=True,
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
        a tuple of its ``attrs`` attributes.  But the attributes are *only*
        compared, if the type of both classes is *identical*!
    :type add_cmp: bool

    :param add_hash: Add a ``__hash__`` method that returns the :func:`hash` of
        a tuple of all ``attrs`` attribute values.
    :type add_hash: bool

    :param add_init: Add a ``__init__`` method that initialiazes the ``attrs``
        attributes.  Leading underscores are stripped for the argument name:.

        .. doctest::

            >>> import attr
            >>> @attr.s
            ... class C(object):
            ...     _private = attr.ib()
            >>> C(private=42)
            C(_private=42)
    :type add_init: bool
    """
    # attrs_or class type depends on the usage of the decorator.  It's a class
    # if it's used as `@attributes` but ``None`` (or a value passed) if used
    # as `@attributes()`.
    if isinstance(maybe_cl, type):
        _transform_attrs(maybe_cl)
        return _add_init(_add_hash(_add_cmp(_add_repr(maybe_cl))))
    else:
        def wrap(cl):
            _transform_attrs(cl)
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
