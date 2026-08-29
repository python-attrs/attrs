# SPDX-License-Identifier: MIT

"""
Tests for `attr.filters`.
"""

import pytest

import attr

from attr import fields
from attr.filters import _split_what, exclude, include


@attr.s
class C:
    a = attr.ib()
    b = attr.ib()


class TestSplitWhat:
    """
    Tests for `_split_what`.
    """

    def test_splits(self):
        """
        Splits correctly.
        """
        assert (
            frozenset((int, str)),
            frozenset(("abcd", "123")),
            frozenset((fields(C).a,)),
        ) == _split_what((str, "123", fields(C).a, int, "abcd"))


class TestInclude:
    """
    Tests for `include`.
    """

    @pytest.mark.parametrize(
        ("incl", "value"),
        [
            ((int,), 42),
            ((str,), "hello"),
            ((str, fields(C).a), 42),
            ((str, fields(C).b), "hello"),
            (("a",), 42),
            (("a",), "hello"),
            (("a", str), 42),
            (("a", fields(C).b), "hello"),
        ],
    )
    def test_allow(self, incl, value):
        """
        Return True if a class or attribute is included.
        """
        i = include(*incl)
        assert i(fields(C).a, value) is True

    @pytest.mark.parametrize(
        ("incl", "value"),
        [
            ((str,), 42),
            ((int,), "hello"),
            ((str, fields(C).b), 42),
            ((int, fields(C).b), "hello"),
            (("b",), 42),
            (("b",), "hello"),
            (("b", str), 42),
            (("b", fields(C).b), "hello"),
        ],
    )
    def test_drop_class(self, incl, value):
        """
        Return False on non-included classes and attributes.
        """
        i = include(*incl)
        assert i(fields(C).a, value) is False


class TestExclude:
    """
    Tests for `exclude`.
    """

    @pytest.mark.parametrize(
        ("excl", "value"),
        [
            ((str,), 42),
            ((int,), "hello"),
            ((str, fields(C).b), 42),
            ((int, fields(C).b), "hello"),
            (("b",), 42),
            (("b",), "hello"),
            (("b", str), 42),
            (("b", fields(C).b), "hello"),
        ],
    )
    def test_allow(self, excl, value):
        """
        Return True if class or attribute is not excluded.
        """
        e = exclude(*excl)
        assert e(fields(C).a, value) is True

    @pytest.mark.parametrize(
        ("excl", "value"),
        [
            ((int,), 42),
            ((str,), "hello"),
            ((str, fields(C).a), 42),
            ((str, fields(C).b), "hello"),
            (("a",), 42),
            (("a",), "hello"),
            (("a", str), 42),
            (("a", fields(C).b), "hello"),
        ],
    )
    def test_drop_class(self, excl, value):
        """
        Return True on non-excluded classes and attributes.
        """
        e = exclude(*excl)
        assert e(fields(C).a, value) is False


@attr.s
class C2:
    a = attr.ib()
    repeated = attr.ib()


@attr.s
class D2:
    b = attr.ib()
    repeated = attr.ib()


class TestSameNameAcrossClasses:
    """
    Two classes may define attributes with the same name but they are
    different `Attribute` instances; excluding one must not exclude the
    other (https://github.com/python-attrs/attrs/issues/864).
    """

    def test_exclude_identity_not_equality(self):
        e = exclude(fields(C2).repeated)
        assert e(fields(C2).repeated, "x") is False
        assert e(fields(D2).repeated, "x") is True

    def test_include_identity_not_equality(self):
        i = include(fields(C2).repeated)
        assert i(fields(C2).repeated, "x") is True
        assert i(fields(D2).repeated, "x") is False
