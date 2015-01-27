# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest

from attr._make import (
    Attribute,
    _CountingAttr,
    _get_attrs,
    _make_attr,
    s,
)


class TestMakeAttr(object):
    """
    Tests for `_make_attr`.
    """
    def test_returns_Attr(self):
        """
        Returns an instance of _Attr.
        """
        a = _make_attr()
        assert isinstance(a, _CountingAttr)

    def test_catches_ambiguous_defaults(self):
        """
        Raises ValueError if both default_value and default_factory are
        specified.
        """
        with pytest.raises(ValueError) as e:
            _make_attr(default_value=42, default_factory=list)

        assert (
            "Specifying both default_value and default_factory is ambiguous."
            == e.value.args[0]
        )


class TestGetAttrs(object):
    """
    Tests for `_get_attrs`.
    """
    def test_normal(self):
        """
        Returns attributes in correct order.
        """
        @s
        class C(object):
            z = _make_attr()
            y = _make_attr()
            x = _make_attr()

        assert ["z", "y", "x"] == [name for (name, _) in _get_attrs(C)]

    def test_empty(self):
        """
        No attributes returns an empty list.
        """
        @s
        class C(object):
            pass

        assert [] == _get_attrs(C)


class TestS(object):
    """
    Tests for the `s` class decorator.
    """
    def test_sets_attrs(self):
        """
        Sets the `__attrs_attrs__` class attribute with a list of `Attribute`s.
        """
        @s
        class C(object):
            x = _make_attr()
        assert "x" == C.__attrs_attrs__[0].name
        assert all(isinstance(a, Attribute) for a in C.__attrs_attrs__)

    def test_empty(self):
        """
        No attributes, no problems.
        """
        @s
        class C3(object):
            pass
        assert "<C3()>" == repr(C3())
        assert C3() == C3()
