# -*- coding: utf-8 -*-

"""
Tests for `attr._make`.
"""

from __future__ import absolute_import, division, print_function

import pytest

from attr._make import (
    Attribute,
    NOTHING,
    _CountingAttr,
    _transform_attrs,
    attr,
    attributes,
    make_class,
)


class TestCountingAttr(object):
    """
    Tests for `attr`.
    """
    def test_returns_Attr(self):
        """
        Returns an instance of _CountingAttr.
        """
        a = attr()
        assert isinstance(a, _CountingAttr)


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

    def test_conflicting_defaults(self):
        """
        Raises `ValueError` if attributes with defaults are followed by
        mandatory attributes.
        """
        class C(object):
            x = attr(default=None)
            y = attr()

        with pytest.raises(ValueError) as e:
            _transform_attrs(C)
        assert (
            "No mandatory attributes allowed after an attribute with a "
            "default value or factory.  Attribute in question: Attribute"
            "(name='y', default=NOTHING, validator=None, no_repr=False, "
            "no_cmp=False, no_hash=False, no_init=False)",
        ) == e.value.args


class TestAttributes(object):
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
        ("no_repr", "__repr__"),
        ("no_cmp", "__eq__"),
        ("no_hash", "__hash__"),
        ("no_init", "__init__"),
    ])
    def test_respects_add_arguments(self, arg_name, method_name):
        """
        If a certain `add_XXX` is `True`, XXX is not added to the class.
        """
        # Set the method name to a sentinel and check whether it has been
        # overwritten afterwards.
        sentinel = object()

        am_args = {
            "no_repr": False,
            "no_cmp": False,
            "no_hash": False,
            "no_init": False
        }
        am_args[arg_name] = True

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
        Raises `TypeError` if an Argument is missing.
        """
        with pytest.raises(TypeError) as e:
            Attribute(default=NOTHING, validator=None)
        assert ("Missing argument 'name'.",) == e.value.args

    def test_too_many_arguments(self):
        """
        Raises `TypeError` if extra arguments are passed.
        """
        with pytest.raises(TypeError) as e:
            Attribute(name="foo", default=NOTHING,
                      factory=NOTHING, validator=None, no_repr=False,
                      no_cmp=False, no_hash=False, no_init=False)
        assert ("Too many arguments.",) == e.value.args


class TestMakeClass(object):
    """
    Tests for `make_class`.
    """
    @pytest.mark.parametrize("ls", [
        list,
        tuple
    ])
    def test_simple(self, ls):
        """
        Passing a list of strings creates attributes with default args.
        """
        C1 = make_class("C1", ls(["a", "b"]))

        @attributes
        class C2(object):
            a = attr()
            b = attr()

        assert C1.__attrs_attrs__ == C2.__attrs_attrs__

    def test_dict(self):
        """
        Passing a dict of name: _CountingAttr creates an equivalent class.
        """
        C1 = make_class("C1", {"a": attr(default=42), "b": attr(default=None)})

        @attributes
        class C2(object):
            a = attr(default=42)
            b = attr(default=None)

        assert C1.__attrs_attrs__ == C2.__attrs_attrs__

    def test_attr_args(self):
        """
        attributes_arguments are passed to attributes
        """
        C = make_class("C", ["x"], no_repr=True)
        assert repr(C(1)).startswith("<attr._make.C object at 0x")

    def test_catches_wrong_attrs_type(self):
        """
        Raise `TypeError` if an invalid type for attrs is passed.
        """
        with pytest.raises(TypeError) as e:
            make_class("C", object())

        assert (
            "attrs argument must be a dict or a list.",
        ) == e.value.args
