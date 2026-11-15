# SPDX-License-Identifier: MIT

"""
Witness tests for the review of PR #1654 (request A1).

A maintainer asked that the member validator of `deep_iterable` receive the
*real* `attrs.Attribute` instance and the real instance, and that the member
name only be formatted where the error is raised -- not handed to the member
validator through a proxy object.

These tests are written *before* the fix and are expected to be RED.
"""

from __future__ import annotations

import pytest

import attr

from attr.validators import deep_iterable


@attr.s(auto_attribs=True, slots=True)
class C:
    x: list = attr.ib(
        validator=deep_iterable(member_validator=lambda *a: None)
    )


def get_attribute():
    """
    Return the real `attr.Attribute` for ``C.x``.
    """
    return attr.fields(C).x


class TestMemberValidatorReceivesTheRealAttribute:
    """
    A1: the member validator gets the real `attr.Attribute` and the real
    instance; the member name is formatted at the raise site only.
    """

    def test_member_validator_sees_real_attribute(self):
        """
        `attr` is the very `Attribute` object of the class (identity), so
        `isinstance(attr, attr.Attribute)` holds and `attr.x` etc. work.
        """
        seen = []
        expected = get_attribute()
        inst = C([1, 2, 3])

        v = deep_iterable(member_validator=lambda i, a, val: seen.append((i, a)))
        v(inst, expected, [1, 2, 3])

        # One call per member, and each one got the real instance/attribute.
        assert [(inst, expected)] * 3 == seen
        for _instance, a in seen:
            assert a is expected
            assert isinstance(a, attr.Attribute)

    def test_member_validator_sees_real_attribute_on_failure(self):
        """
        The identity holds even when the member validator raises.
        """
        seen = []
        expected = get_attribute()

        def member_validator(instance, attribute, value):
            seen.append(attribute)
            if value == 2:
                msg = "'{name}' must not be 2."
                raise ValueError(msg.format(name=attribute.name))

        v = deep_iterable(member_validator=member_validator)

        with pytest.raises(ValueError):
            v(None, expected, [1, 2, 3])

        assert expected is seen[0]
        assert isinstance(seen[0], attr.Attribute)

    def test_error_message_still_names_the_member(self):
        """
        The message raised by the member validator is still re-prefixed with
        the member name: ``x[1]``, not ``x``.
        """
        expected = get_attribute()

        def member_validator(instance, attribute, value):
            if value == 2:
                msg = "'{name}' must not be 2."
                raise ValueError(msg.format(name=attribute.name))

        v = deep_iterable(member_validator=member_validator)

        with pytest.raises(ValueError) as ei:
            v(None, expected, [1, 2, 3])

        # The validator formatted the *whole* attribute name, the raise site
        # must point at the member that failed.
        assert "'x[1]' must not be 2." == ei.value.args[0]


class TestDeepIterableEnumerateOverDict:
    """
    A3: nit -- `enumerate(value)` over a `dict` yields positional indices
    (`x[0]`) instead of the key (`x['k']`).
    """

    def test_dict_member_error_names_the_key(self):
        """
        For a mapping, the failing member is named by its key.
        """
        expected = get_attribute()

        v = deep_iterable(member_validator=instance_of_str)

        with pytest.raises(TypeError) as ei:
            v(None, expected, {"a": "ok", "b": 42})

        assert (
            "'x['b']' must be <class 'str'> (got 42 that is a <class 'int'>)."
            == ei.value.args[0]
        )


def instance_of_str(instance, attribute, value):
    if not isinstance(value, str):
        msg = "'{name}' must be <class 'str'> (got {value!r} that is a {actual!r})."
        raise TypeError(
            msg.format(
                name=attribute.name, value=value, actual=value.__class__
            )
        )
