# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ._make import _make_attr, _add_methods


@_add_methods(add_repr=False)
class _InstanceOfValidator(object):
    type_ = _make_attr()

    def __call__(self, attr, value):
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
