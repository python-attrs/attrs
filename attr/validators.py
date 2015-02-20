"""
Commonly useful validators.
"""

from __future__ import absolute_import, division, print_function

from ._make import attr, attributes


@attributes(repr=False)
class _InstanceOfValidator(object):
    type_ = attr()

    def __call__(self, inst, attr, value):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        if not isinstance(value, self.type_):
            raise TypeError(
                "'{name}' must be {type!r} (got {value!r} that is a "
                "{actual!r})."
                .format(name=attr.name, type=self.type_,
                        actual=value.__class__, value=value),
                attr, self.type_, value,
            )

    def __repr__(self):
        return (
            "<instance_of validator for type {type!r}>"
            .format(type=self.type_)
        )


def instance_of(type_):
    """
    A validator that raises a :exc:`TypeError` if the initializer is called
    with a wrong type for this particular attribute (checks are perfomed using
    :func:`isinstance`).

    :param type_: The type to check for.
    :type type_: type

    The :exc:`TypeError` is raised with a human readable error message, the
    attribute (of type :class:`attr.Attribute`), the expected type and the
    value it got.
    """
    return _InstanceOfValidator(type_)


@attributes(repr=False)
class _ProvidesValidator(object):
    interface = attr()

    def __call__(self, inst, attr, value):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        if not self.interface.providedBy(value):
            raise TypeError(
                "'{name}' must provide {interface!r} which {value!r} "
                "doesn't."
                .format(name=attr.name, interface=self.interface, value=value),
                attr, self.interface, value,
            )

    def __repr__(self):
        return (
            "<provides validator for interface {interface!r}>"
            .format(interface=self.interface)
        )


def provides(interface):
    """
    A validator that raises a :exc:`TypeError` if the initializer is called
    with an object that does not provide the requested *interface* (checks are
    perfomed using ``value.providedBy(interface)`` (see `zope.interface
    <http://docs.zope.org/zope.interface/>`_).

    :param type_: The interface to check for.
    :type type_: zope.interface.Interface

    The :exc:`TypeError` is raised with a human readable error message, the
    attribute (of type :class:`attr.Attribute`), the expected interface, and
    the value it got.
    """
    return _ProvidesValidator(interface)
