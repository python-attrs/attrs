"""
Tests for `attr._make`.
"""

from __future__ import absolute_import, division, print_function

import inspect

from operator import attrgetter

import pytest

from hypothesis import given
from hypothesis.strategies import booleans, integers, lists, sampled_from, text

from attr import _config
from attr._compat import PY2
from attr._make import (
    Attribute,
    Factory,
    _AndValidator,
    _CountingAttr,
    _transform_attrs,
    and_,
    attr,
    attributes,
    fields,
    make_class,
    validate,
)
from attr.exceptions import NotAnAttrsClassError, DefaultAlreadySetError

from .utils import (gen_attr_names, list_of_attrs, simple_attr, simple_attrs,
                    simple_attrs_without_metadata, simple_classes)

attrs = simple_attrs.map(lambda c: Attribute.from_counting_attr("name", c))


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

    def _test_validator_none_is_empty_tuple(self):
        """
        If validator is None, it's transformed into an empty tuple.
        """
        a = attr(validator=None)

        assert () == a._validator

    def test_validators_lists_to_wrapped_tuples(self):
        """
        If a list is passed as validator, it's just converted to a tuple.
        """
        def v1(_, __):
            pass

        def v2(_, __):
            pass

        a = attr(validator=[v1, v2])

        assert _AndValidator((v1, v2,)) == a._validator

    def test_validator_decorator_single(self):
        """
        If _CountingAttr.validator is used as a decorator and there is no
        decorator set, the decorated method is used as the validator.
        """
        a = attr()

        @a.validator
        def v():
            pass

        assert v == a._validator

    @pytest.mark.parametrize("wrap", [
        lambda v: v,
        lambda v: [v],
        lambda v: and_(v)

    ])
    def test_validator_decorator(self, wrap):
        """
        If _CountingAttr.validator is used as a decorator and there is already
        a decorator set, the decorators are composed using `and_`.
        """
        def v(_, __):
            pass

        a = attr(validator=wrap(v))

        @a.validator
        def v2(self, _, __):
            pass

        assert _AndValidator((v, v2,)) == a._validator

    def test_default_decorator_already_set(self):
        """
        Raise DefaultAlreadySetError if the decorator is used after a default
        has been set.
        """
        a = attr(default=42)

        with pytest.raises(DefaultAlreadySetError):
            @a.default
            def f(self):
                pass

    def test_default_decorator_sets(self):
        """
        Decorator wraps the method in a Factory with pass_self=True and sets
        the default.
        """
        a = attr()

        @a.default
        def f(self):
            pass

        assert Factory(f, True) == a._default


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
            "cmp=True, hash=None, init=True, convert=None, "
            "metadata=mappingproxy({}))",
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
    Tests for the `attrs`/`attr.s` class decorator.
    """
    @pytest.mark.skipif(not PY2, reason="No old-style classes in Py3")
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

    @given(attr=attrs, attr_name=sampled_from(Attribute.__slots__))
    def test_immutable(self, attr, attr_name):
        """
        Attribute instances are immutable.
        """
        with pytest.raises(AttributeError):
            setattr(attr, attr_name, 1)

    @pytest.mark.parametrize("method_name", [
        "__repr__",
        "__eq__",
        "__hash__",
        "__init__",
    ])
    def test_adds_all_by_default(self, method_name):
        """
        If no further arguments are supplied, all add_XXX functions except
        add_hash are applied.  __hash__ is set to None.
        """
        # Set the method name to a sentinel and check whether it has been
        # overwritten afterwards.
        sentinel = object()

        class C(object):
            x = attr()

        setattr(C, method_name, sentinel)

        C = attributes(C)
        meth = getattr(C, method_name)

        assert sentinel != meth
        if method_name == "__hash__":
            assert meth is None

    @pytest.mark.parametrize("arg_name, method_name", [
        ("repr", "__repr__"),
        ("cmp", "__eq__"),
        ("hash", "__hash__"),
        ("init", "__init__"),
    ])
    def test_respects_add_arguments(self, arg_name, method_name):
        """
        If a certain `add_XXX` is `False`, `__XXX__` is not added to the class.
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

    @pytest.mark.skipif(PY2, reason="__qualname__ is PY3-only.")
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

    @pytest.mark.skipif(PY2, reason="__qualname__ is PY3-only.")
    @given(slots_outer=booleans(), slots_inner=booleans())
    def test_name_not_overridden(self, slots_outer, slots_inner):
        """
        On Python 3, __name__ is different from __qualname__.
        """
        @attributes(slots=slots_outer)
        class C(object):
            @attributes(slots=slots_inner)
            class D(object):
                pass

        assert C.D.__name__ == "D"
        assert C.D.__qualname__ == C.__qualname__ + ".D"

    @given(with_validation=booleans())
    def test_post_init(self, with_validation, monkeypatch):
        """
        Verify that __attrs_post_init__ gets called if defined.
        """
        monkeypatch.setattr(_config, "_run_validators", with_validation)

        @attributes
        class C(object):
            x = attr()
            y = attr()

            def __attrs_post_init__(self2):
                self2.z = self2.x + self2.y

        c = C(x=10, y=20)
        assert 30 == getattr(c, 'z', None)


@attributes
class GC(object):
    @attributes
    class D(object):
        pass


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

    def test_bases(self):
        """
        Parameter bases default to (object,) and subclasses correctly
        """
        class D(object):
            pass

        cls = make_class("C", {})
        assert cls.__mro__[-1] == object

        cls = make_class("C", {}, bases=(D,))
        assert D in cls.__mro__
        assert isinstance(cls(), D)


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
        with pytest.raises(NotAnAttrsClassError) as e:
            fields(object)
        assert (
            "{o!r} is not an attrs-decorated class.".format(o=object)
        ) == e.value.args[0]

    @given(simple_classes())
    def test_fields(self, C):
        """
        Returns a list of `Attribute`a.
        """
        assert all(isinstance(a, Attribute) for a in fields(C))

    @given(simple_classes())
    def test_fields_properties(self, C):
        """
        Fields returns a tuple with properties.
        """
        for attribute in fields(C):
            assert getattr(fields(C), attribute.name) is attribute


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

    @given(integers(), booleans())
    def test_convert_property(self, val, init):
        """
        Property tests for attributes with convert.
        """
        C = make_class("C", {"y": attr(),
                             "x": attr(init=init, default=val,
                                       convert=lambda v: v + 1),
                             })
        c = C(2)
        assert c.x == val + 1
        assert c.y == 2

    @given(integers(), booleans())
    def test_convert_factory_property(self, val, init):
        """
        Property tests for attributes with convert, and a factory default.
        """
        C = make_class("C", {"y": attr(),
                             "x": attr(init=init,
                                       default=Factory(lambda: val),
                                       convert=lambda v: v + 1),
                             })
        c = C(2)
        assert c.x == val + 1
        assert c.y == 2

    def test_factory_takes_self(self):
        """
        If takes_self on factories is True, self is passed.
        """
        C = make_class("C", {"x": attr(default=Factory(
            (lambda self: self), takes_self=True
        ))})

        i = C()

        assert i is i.x

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

    def test_frozen(self):
        """
        Converters circumvent immutability.
        """
        C = make_class("C", {"x": attr(convert=lambda v: int(v))}, frozen=True)
        C("1")


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
        c = C(1)
        validate(c)
        assert 1 == c.x
        _config._run_validators = True

        with pytest.raises(Exception):
            validate(c)

        with pytest.raises(Exception) as e:
            C(1)
        assert (obj,) == e.value.args

    def test_multiple_validators(self):
        """
        If a list is passed as a validator, all of its items are treated as one
        and must pass.
        """
        def v1(_, __, value):
            if value == 23:
                raise TypeError("omg")

        def v2(_, __, value):
            if value == 42:
                raise ValueError("omg")

        C = make_class("C", {"x": attr(validator=[v1, v2])})

        validate(C(1))

        with pytest.raises(TypeError) as e:
            C(23)

        assert "omg" == e.value.args[0]

        with pytest.raises(ValueError) as e:
            C(42)

        assert "omg" == e.value.args[0]

    def test_multiple_empty(self):
        """
        Empty list/tuple for validator is the same as None.
        """
        C1 = make_class("C", {"x": attr(validator=[])})
        C2 = make_class("C", {"x": attr(validator=None)})

        assert inspect.getsource(C1.__init__) == inspect.getsource(C2.__init__)


# Hypothesis seems to cache values, so the lists of attributes come out
# unsorted.
sorted_lists_of_attrs = list_of_attrs.map(
    lambda l: sorted(l, key=attrgetter("counter")))


class TestMetadata(object):
    """
    Tests for metadata handling.
    """
    @given(sorted_lists_of_attrs)
    def test_metadata_present(self, list_of_attrs):
        """
        Assert dictionaries are copied and present.
        """
        C = make_class("C", dict(zip(gen_attr_names(), list_of_attrs)))

        for hyp_attr, class_attr in zip(list_of_attrs, fields(C)):
            if hyp_attr.metadata is None:
                # The default is a singleton empty dict.
                assert class_attr.metadata is not None
                assert len(class_attr.metadata) == 0
            else:
                assert hyp_attr.metadata == class_attr.metadata

                # Once more, just to assert getting items and iteration.
                for k in class_attr.metadata:
                    assert hyp_attr.metadata[k] == class_attr.metadata[k]
                    assert (hyp_attr.metadata.get(k) ==
                            class_attr.metadata.get(k))

    @given(simple_classes(), text())
    def test_metadata_immutability(self, C, string):
        """
        The metadata dict should be best-effort immutable.
        """
        for a in fields(C):
            with pytest.raises(TypeError):
                a.metadata[string] = string
            with pytest.raises(AttributeError):
                a.metadata.update({string: string})
            with pytest.raises(AttributeError):
                a.metadata.clear()
            with pytest.raises(AttributeError):
                a.metadata.setdefault(string, string)

            for k in a.metadata:
                # For some reason, Python 3's MappingProxyType throws an
                # IndexError for deletes on a large integer key.
                with pytest.raises((TypeError, IndexError)):
                    del a.metadata[k]
                with pytest.raises(AttributeError):
                    a.metadata.pop(k)
            with pytest.raises(AttributeError):
                    a.metadata.popitem()

    @given(lists(simple_attrs_without_metadata, min_size=2, max_size=5))
    def test_empty_metadata_singleton(self, list_of_attrs):
        """
        All empty metadata attributes share the same empty metadata dict.
        """
        C = make_class("C", dict(zip(gen_attr_names(), list_of_attrs)))
        for a in fields(C)[1:]:
            assert a.metadata is fields(C)[0].metadata
