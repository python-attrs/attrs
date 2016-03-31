"""
Tests for `attr._make`.
"""

from __future__ import absolute_import, division, print_function

import pytest
from hypothesis import given
from hypothesis.strategies import booleans

from . import simple_attr
from attr import _config
from attr._compat import PY3
from attr._make import (
    Attribute,
    NOTHING,
    _CountingAttr,
    _transform_attrs,
    attr,
    attributes,
    fields,
    make_class,
    validate,
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
        _transform_attrs(C, None)
        assert ["z", "y", "x"] == [a.name for a in C.__attrs_attrs__]

    def test_empty(self):
        """
        No attributes works as expected.
        """
        @attributes
        class C(object):
            pass

        _transform_attrs(C, None)

        assert () == C.__attrs_attrs__

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
        _transform_attrs(C, None)

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
            _transform_attrs(C, None)
        assert (
            "No mandatory attributes allowed after an attribute with a "
            "default value or factory.  Attribute in question: Attribute"
            "(name='y', default=NOTHING, validator=None, repr=True, "
            "cmp=True, hash=True, init=True, convert=None)",
        ) == e.value.args

    def test_these(self):
        """
        If these is passed, use it and ignore body.
        """
        class C(object):
            y = attr()

        _transform_attrs(C, {"x": attr()})
        assert (
            simple_attr("x"),
        ) == C.__attrs_attrs__
        assert isinstance(C.y, _CountingAttr)

    def test_recurse(self):
        """
        Collect attributes from all sub-classes.
        """
        class A(object):
            a = None

        class B(A):
            b = attr()

        _transform_attrs(B, None)

        class C(B):
            c = attr()

        _transform_attrs(C, None)

        class D(C):
            d = attr()

        _transform_attrs(D, None)

        class E(D):
            e = attr()

        _transform_attrs(E, None)

        assert (
            simple_attr("b"),
            simple_attr("c"),
            simple_attr("d"),
            simple_attr("e"),
        ) == E.__attrs_attrs__


class TestAttributes(object):
    """
    Tests for the `attributes` class decorator.
    """
    @pytest.mark.skipif(PY3, reason="No old-style classes in Py3")
    def test_catches_old_style(self):
        """
        Raises TypeError on old-style classes.
        """
        with pytest.raises(TypeError) as e:
            @attributes
            class C:
                pass
        assert ("attrs only works with new-style classes.",) == e.value.args

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
        ("repr", "__repr__"),
        ("cmp", "__eq__"),
        ("hash", "__hash__"),
        ("init", "__init__"),
    ])
    def test_respects_add_arguments(self, arg_name, method_name):
        """
        If a certain `add_XXX` is `True`, XXX is not added to the class.
        """
        # Set the method name to a sentinel and check whether it has been
        # overwritten afterwards.
        sentinel = object()

        am_args = {
            "repr": True,
            "cmp": True,
            "hash": True,
            "init": True
        }
        am_args[arg_name] = False

        class C(object):
            x = attr()

        setattr(C, method_name, sentinel)

        C = attributes(**am_args)(C)

        assert sentinel == getattr(C, method_name)

    @pytest.mark.skipif(not PY3, reason="__qualname__ is PY3-only.")
    @given(slots_outer=booleans(), slots_inner=booleans())
    def test_repr_qualname(self, slots_outer, slots_inner):
        """
        On Python 3, the name in repr is the __qualname__.
        """
        @attributes(slots=slots_outer)
        class C(object):
            @attributes(slots=slots_inner)
            class D(object):
                pass

        assert "C.D()" == repr(C.D())
        assert "GC.D()" == repr(GC.D())

    @given(slots_outer=booleans(), slots_inner=booleans())
    def test_repr_fake_qualname(self, slots_outer, slots_inner):
        """
        Setting repr_ns overrides a potentially guessed namespace.
        """
        @attributes(slots=slots_outer)
        class C(object):
            @attributes(repr_ns="C", slots=slots_inner)
            class D(object):
                pass
        assert "C.D()" == repr(C.D())


@attributes
class GC(object):
    @attributes
    class D(object):
        pass


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
                      factory=NOTHING, validator=None,
                      repr=True, cmp=True, hash=True, init=True, convert=None)
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
        C = make_class("C", ["x"], repr=False)
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


class TestFields(object):
    """
    Tests for `fields`.
    """
    def test_instance(self, C):
        """
        Raises `TypeError` on non-classes.
        """
        with pytest.raises(TypeError) as e:
            fields(C(1, 2))
        assert "Passed object must be a class." == e.value.args[0]

    def test_handler_non_attrs_class(self, C):
        """
        Raises `ValueError` if passed a non-``attrs`` instance.
        """
        with pytest.raises(ValueError) as e:
            fields(object)
        assert (
            "{o!r} is not an attrs-decorated class.".format(o=object)
        ) == e.value.args[0]

    def test_fields(self, C):
        """
        Returns a list of `Attribute`a.
        """
        assert all(isinstance(a, Attribute) for a in fields(C))

    def test_copies(self, C):
        """
        Returns a new list object with new `Attribute` objects.
        """
        assert C.__attrs_attrs__ is not fields(C)
        assert all(new == original and new is not original
                   for new, original
                   in zip(fields(C), C.__attrs_attrs__))


class TestConvert(object):
    """
    Tests for attribute conversion.
    """
    def test_convert(self):
        """
        Return value of convert is used as the attribute's value.
        """
        C = make_class("C", {"x": attr(convert=lambda v: v + 1),
                             "y": attr()})
        c = C(1, 2)
        assert c.x == 2
        assert c.y == 2

    def test_convert_before_validate(self):
        """
        Validation happens after conversion.
        """
        def validator(inst, attr, val):
            raise RuntimeError("foo")
        C = make_class(
            "C",
            {"x": attr(validator=validator, convert=lambda v: 1 / 0),
             "y": attr()})
        with pytest.raises(ZeroDivisionError):
            C(1, 2)


class TestValidate(object):
    """
    Tests for `validate`.
    """
    def test_success(self):
        """
        If the validator suceeds, nothing gets raised.
        """
        C = make_class("C", {"x": attr(validator=lambda *a: None),
                             "y": attr()})
        validate(C(1, 2))

    def test_propagates(self):
        """
        The exception of the validator is handed through.
        """
        def raiser(_, __, value):
            if value == 42:
                raise FloatingPointError

        C = make_class("C", {"x": attr(validator=raiser)})
        i = C(1)
        i.x = 42

        with pytest.raises(FloatingPointError):
            validate(i)

    def test_run_validators(self):
        """
        Setting `_run_validators` to False prevents validators from running.
        """
        _config._run_validators = False
        obj = object()

        def raiser(_, __, ___):
            raise Exception(obj)

        C = make_class("C", {"x": attr(validator=raiser)})
        assert 1 == C(1).x
        _config._run_validators = True

        with pytest.raises(Exception) as e:
            C(1)
        assert (obj,) == e.value.args
