# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest

from attr._dunders import NOTHING
from attr._make import (
    Attribute,
    _CountingAttr,
    attributes,
    attr,
    _transform_attrs,
)


class TestMakeAttr(object):
    """
    Tests for `attr`.
    """
    def test_returns_Attr(self):
        """
        Returns an instance of _Attr.
        """
        a = attr()
        assert isinstance(a, _CountingAttr)

    def test_catches_ambiguous_defaults(self):
        """
        Raises ValueError if both default_value and default_factory are
        specified.
        """
        with pytest.raises(ValueError) as e:
            attr(default_value=42, default_factory=list)

        assert (
            "Specifying both default_value and default_factory is ambiguous."
            == e.value.args[0]
        )


def make_tc():
    class TransformC(object):
        z = attr()
        y = attr()
        x = attr()
        a = 42
    return TransformC


class TestTransformAttrs(object):
    """
    Tests for `_transform_attrs`.
    """
    def test_normal(self):
        """
        Transforms every `_CountingAttr` and leaves others (a) be.
        """
        C = make_tc()
        _transform_attrs(C)
        assert ["z", "y", "x"] == [a.name for a in C.__attrs_attrs__]

    def test_empty(self):
        """
        No attributes works as expected.
        """
        @attributes
        class C(object):
            pass

        _transform_attrs(C)

        assert [] == C.__attrs_attrs__

    @pytest.mark.parametrize("attribute", [
        "z",
        "y",
        "x",
    ])
    def test_transforms_to_attribute(self, attribute):
        """
        All `_CountingAttr`s are transformed into `Attribute`s.
        """
        C = make_tc()
        _transform_attrs(C)

        assert isinstance(getattr(C, attribute), Attribute)


class TestAddMethods(object):
    """
    Tests for the `attributes` class decorator.
    """
    def test_sets_attrs(self):
        """
        Sets the `__attrs_attrs__` class attribute with a list of `Attribute`s.
        """
        @attributes
        class C(object):
            x = attr()
        assert "x" == C.__attrs_attrs__[0].name
        assert all(isinstance(a, Attribute) for a in C.__attrs_attrs__)

    def test_empty(self):
        """
        No attributes, no problems.
        """
        @attributes
        class C3(object):
            pass
        assert "C3()" == repr(C3())
        assert C3() == C3()

    @pytest.mark.parametrize("method_name", [
        "__repr__",
        "__eq__",
        "__hash__",
        "__init__",
    ])
    def test_adds_all_by_default(self, method_name):
        """
        If no further arguments are supplied, all add_XXX functions are
        applied.
        """
        # Set the method name to a sentinel and check whether it has been
        # overwritten afterwards.
        sentinel = object()

        class C1(object):
            x = attr()

        setattr(C1, method_name, sentinel)

        C1 = attributes(C1)

        class C2(object):
            x = attr()

        setattr(C2, method_name, sentinel)

        C2 = attributes(C2)

        assert sentinel != getattr(C1, method_name)
        assert sentinel != getattr(C2, method_name)

    @pytest.mark.parametrize("arg_name, method_name", [
        ("add_repr", "__repr__"),
        ("add_cmp", "__eq__"),
        ("add_hash", "__hash__"),
        ("add_init", "__init__"),
    ])
    def test_respects_add_arguments(self, arg_name, method_name):
        """
        If a certain `add_XXX` is `True`, XXX is not added to the class.
        """
        # Set the method name to a sentinel and check whether it has been
        # overwritten afterwards.
        sentinel = object()

        am_args = {
            "add_repr": True,
            "add_cmp": True,
            "add_hash": True,
            "add_init": True
        }
        am_args[arg_name] = False

        class C(object):
            x = attr()

        setattr(C, method_name, sentinel)

        C = attributes(**am_args)(C)

        assert sentinel == getattr(C, method_name)


class TestAttribute(object):
    """
    Tests for `Attribute`.
    """
    def test_missing_argument(self):
        """
        Raises TypeError if an Argument is missing.
        """
        with pytest.raises(TypeError) as e:
            Attribute(default_value=NOTHING, default_factory=NOTHING,
                      validator=None)
        assert ("Missing argument 'name'.",) == e.value.args
