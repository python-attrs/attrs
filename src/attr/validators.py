"""
Commonly useful validators.
"""

from __future__ import absolute_import, division, print_function

from ._make import attr, attributes


@attributes(repr=False, slots=True)
class _MatcherValidator(object):
    matcher = attr()

    def __call__(self, inst, attr, value):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        mismatch = self.matcher.match(value)
        if mismatch is not None:
            raise TypeError("'{}' is invalid: {}".format(attr.name, mismatch.describe()))


def matches(matcher):
    """
    A validator that raises a :exc:`TypeError` if the initializer is
    called with a value which is not matched by a testtools-style
    matcher.

    :param matcher: The matcher to apply to values.

    The :exc:`TypeError` is raised with the matcher-supplied description.

    :see: http://testtools.readthedocs.io/en/latest/for-test-authors.html#matchers
    """
    return _MatcherValidator(matcher)


@attributes(repr=False, slots=True)
class _InstanceOfValidator(object):
    type = attr()

    def __call__(self, inst, attr, value):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        if not isinstance(value, self.type):
            raise TypeError(
                "'{name}' must be {type!r} (got {value!r} that is a "
                "{actual!r})."
                .format(name=attr.name, type=self.type,
                        actual=value.__class__, value=value),
                attr, self.type, value,
            )

    def __repr__(self):
        return (
            "<instance_of validator for type {type!r}>"
            .format(type=self.type)
        )


def instance_of(type):
    """
    A validator that raises a :exc:`TypeError` if the initializer is called
    with a wrong type for this particular attribute (checks are perfomed using
    :func:`isinstance` therefore it's also valid to pass a tuple of types).

    :param type: The type to check for.
    :type type: type or tuple of types

    The :exc:`TypeError` is raised with a human readable error message, the
    attribute (of type :class:`attr.Attribute`), the expected type, and the
    value it got.
    """
    return _InstanceOfValidator(type)


@attributes(repr=False, slots=True)
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
    performed using ``interface.providedBy(value)`` (see `zope.interface
    <https://zopeinterface.readthedocs.io/en/latest/>`_).

    :param zope.interface.Interface interface: The interface to check for.

    The :exc:`TypeError` is raised with a human readable error message, the
    attribute (of type :class:`attr.Attribute`), the expected interface, and
    the value it got.
    """
    return _ProvidesValidator(interface)


@attributes(repr=False, slots=True)
class _OptionalValidator(object):
    validator = attr()

    def __call__(self, inst, attr, value):
        if value is None:
            return
        return self.validator(inst, attr, value)

    def __repr__(self):
        return (
            "<optional validator for {type} or None>"
            .format(type=repr(self.validator))
        )


def optional(validator):
    """
    A validator that makes an attribute optional.  An optional attribute is one
    which can be set to ``None`` in addition to satisfying the requirements of
    the sub-validator.

    :param validator: A validator that is used for non-``None`` values.
    """
    return _OptionalValidator(validator)
