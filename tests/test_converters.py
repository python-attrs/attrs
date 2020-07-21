"""
Tests for `attr.converters`.
"""

from __future__ import absolute_import

from distutils.util import strtobool

import pytest

import attr

from attr import Factory, attrib
from attr.converters import default_if_none, optional, pipe


class TestOptional(object):
    """
    Tests for `optional`.
    """

    def test_success_with_type(self):
        """
        Wrapped converter is used as usual if value is not None.
        """
        c = optional(int)

        assert c("42") == 42

    def test_success_with_none(self):
        """
        Nothing happens if None.
        """
        c = optional(int)

        assert c(None) is None

    def test_fail(self):
        """
        Propagates the underlying conversion error when conversion fails.
        """
        c = optional(int)

        with pytest.raises(ValueError):
            c("not_an_int")


class TestDefaultIfNone(object):
    def test_missing_default(self):
        """
        Raises TypeError if neither default nor factory have been passed.
        """
        with pytest.raises(TypeError, match="Must pass either"):
            default_if_none()

    def test_too_many_defaults(self):
        """
        Raises TypeError if both default and factory are passed.
        """
        with pytest.raises(TypeError, match="but not both"):
            default_if_none(True, lambda: 42)

    def test_factory_takes_self(self):
        """
        Raises ValueError if passed Factory has takes_self=True.
        """
        with pytest.raises(ValueError, match="takes_self"):
            default_if_none(Factory(list, takes_self=True))

    @pytest.mark.parametrize("val", [1, 0, True, False, "foo", "", object()])
    def test_not_none(self, val):
        """
        If a non-None value is passed, it's handed down.
        """
        c = default_if_none("nope")

        assert val == c(val)

        c = default_if_none(factory=list)

        assert val == c(val)

    def test_none_value(self):
        """
        Default values are returned when a None is passed.
        """
        c = default_if_none(42)

        assert 42 == c(None)

    def test_none_factory(self):
        """
        Factories are used if None is passed.
        """
        c = default_if_none(factory=list)

        assert [] == c(None)

        c = default_if_none(default=Factory(list))

        assert [] == c(None)


class TestPipe(object):
    def test_success(self):
        """
        Succeeds if all wrapped converters succeed.
        """
        c = pipe(str, strtobool, bool)

        assert True is c("True") is c(True)

    def test_fail(self):
        """
        Fails if any wrapped converter fails.
        """
        c = pipe(str, strtobool)

        # First wrapped converter fails:
        with pytest.raises(ValueError):
            c(33)

        # Last wrapped converter fails:
        with pytest.raises(ValueError):
            c("33")

    def test_sugar(self):
        """
        `pipe(c1, c2, c3)` and `[c1, c2, c3]` are equivalent.
        """

        @attr.s
        class C(object):
            a1 = attrib(default="True", converter=pipe(str, strtobool, bool))
            a2 = attrib(default=True, converter=[str, strtobool, bool])

        c = C()
        assert True is c.a1 is c.a2
