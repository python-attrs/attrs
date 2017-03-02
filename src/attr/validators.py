"""
Commonly useful validators.
"""

from __future__ import absolute_import, division, print_function

from ._make import attr, attributes


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

    :param interface: The interface to check for.
    :type interface: zope.interface.Interface

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


@attr.s(repr=False, slots=True)
class _AndValidator(object):
    validators = attr.ib()

    def __call__(self, inst, attr, value):
        for v in self.validators:
            v(inst, attr, value)
        return

    def __repr__(self):
        return (
            "<validator sequence : {seq}>".format(seq=repr(self.validators))
        )


def chain(*validators):
    """
    A validator that applies several validators in order

    :param validators: A sequence of validators
    """
    return _AndValidator(validators)


def _guess_type_from_validator(validator):
    """
    Utility method to return the declared type of an attribute or None. It handles _OptionalValidator and _AndValidator
    in order to unpack the validators.

    :param validator:
    :return: the type of attribute declared in an inner 'instance_of' validator (if any is found, the first one is used)
    or None if no inner 'instance_of' validator is found
    """
    if isinstance(validator, _OptionalValidator):
        # Optional : look inside
        return _guess_type_from_validator(validator)

    elif isinstance(validator, _AndValidator):
        # Sequence : try each of them
        for v in validator.validators:
            typ = _guess_type_from_validator(v)
            if typ is not None:
                return typ
        return None

    elif isinstance(validator, _InstanceOfValidator):
        # InstanceOf validator : found it !
        return validator.type

    else:
        # we could not find the type
        return None


def guess_type_from_validators(attr):
    """
    Utility method to return the declared type of an attribute or None. It handles _OptionalValidator and _AndValidator
    in order to unpack the validators.

    :param attr:
    :return: the type of attribute declared in an inner 'instance_of' validator (if any is found, the first one is used)
    or None if no inner 'instance_of' validator is found
    """
    return _guess_type_from_validator(attr.validator)


def is_mandatory(attr):
    """
    Helper method to find if an attribute is mandatory, by checking if its validator is 'optional' or not.

    :param attr:
    :return:
    """
    return not isinstance(attr.validator, _OptionalValidator)
