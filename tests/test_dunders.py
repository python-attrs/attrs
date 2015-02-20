"""
Tests for dunder methods from `attrib._make`.
"""

from __future__ import absolute_import, division, print_function

import copy

import pytest

from . import simple_attr, simple_class
from attr._compat import PY26
from attr._make import (
    Factory,
    NOTHING,
    _Nothing,
    _add_init,
    _add_repr,
    attr,
    make_class,
)
from attr.validators import instance_of


CmpC = simple_class(cmp=True)
ReprC = simple_class(repr=True)
HashC = simple_class(hash=True)


class InitC(object):
    __attrs_attrs__ = [simple_attr("a"), simple_attr("b")]

InitC = _add_init(InitC)


class TestAddCmp(object):
    """
    Tests for `_add_cmp`.
    """
    def test_cmp(self):
        """
        If `cmp` is False, ignore that attribute.
        """
        C = make_class("C", {"a": attr(cmp=False), "b": attr()})

        assert C(1, 2) == C(2, 2)

    def test_equal(self):
        """
        Equal objects are detected as equal.
        """
        assert CmpC(1, 2) == CmpC(1, 2)
        assert not (CmpC(1, 2) != CmpC(1, 2))

    def test_unequal_same_class(self):
        """
        Unequal objects of correct type are detected as unequal.
        """
        assert CmpC(1, 2) != CmpC(2, 1)
        assert not (CmpC(1, 2) == CmpC(2, 1))

    def test_unequal_different_class(self):
        """
        Unequal objects of differnt type are detected even if their attributes
        match.
        """
        class NotCmpC(object):
            a = 1
            b = 2
        assert CmpC(1, 2) != NotCmpC()
        assert not (CmpC(1, 2) == NotCmpC())

    def test_lt(self):
        """
        __lt__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((1, 2),  (2, 1)),
            ((1, 2),  (1, 3)),
            (("a", "b"), ("b", "a")),
        ]:
            assert CmpC(*a) < CmpC(*b)

    def test_lt_unordable(self):
        """
        __lt__ returns NotImplemented if classes differ.
        """
        assert NotImplemented == (CmpC(1, 2).__lt__(42))

    def test_le(self):
        """
        __le__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((1, 2),  (2, 1)),
            ((1, 2),  (1, 3)),
            ((1, 1),  (1, 1)),
            (("a", "b"), ("b", "a")),
            (("a", "b"), ("a", "b")),
        ]:
            assert CmpC(*a) <= CmpC(*b)

    def test_le_unordable(self):
        """
        __le__ returns NotImplemented if classes differ.
        """
        assert NotImplemented == (CmpC(1, 2).__le__(42))

    def test_gt(self):
        """
        __gt__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((2, 1), (1, 2)),
            ((1, 3), (1, 2)),
            (("b", "a"), ("a", "b")),
        ]:
            assert CmpC(*a) > CmpC(*b)

    def test_gt_unordable(self):
        """
        __gt__ returns NotImplemented if classes differ.
        """
        assert NotImplemented == (CmpC(1, 2).__gt__(42))

    def test_ge(self):
        """
        __ge__ compares objects as tuples of attribute values.
        """
        for a, b in [
            ((2, 1), (1, 2)),
            ((1, 3), (1, 2)),
            ((1, 1), (1, 1)),
            (("b", "a"), ("a", "b")),
            (("a", "b"), ("a", "b")),
        ]:
            assert CmpC(*a) >= CmpC(*b)

    def test_ge_unordable(self):
        """
        __ge__ returns NotImplemented if classes differ.
        """
        assert NotImplemented == (CmpC(1, 2).__ge__(42))


class TestAddRepr(object):
    """
    Tests for `_add_repr`.
    """
    def test_repr(self):
        """
        If `repr` is False, ignore that attribute.
        """
        C = make_class("C", {"a": attr(repr=False), "b": attr()})

        assert "C(b=2)" == repr(C(1, 2))

    def test_repr_works(self):
        """
        repr returns a sensible value.
        """
        assert "C(a=1, b=2)" == repr(ReprC(1, 2))

    def test_underscores(self):
        """
        repr does not strip underscores.
        """
        class C(object):
            __attrs_attrs__ = [simple_attr("_x")]

        C = _add_repr(C)
        i = C()
        i._x = 42

        assert "C(_x=42)" == repr(i)


class TestAddHash(object):
    """
    Tests for `_add_hash`.
    """
    def test_hash(self):
        """
        If `hash` is False, ignore that attribute.
        """
        C = make_class("C", {"a": attr(hash=False), "b": attr()})

        assert hash(C(1, 2)) == hash(C(2, 2))

    def test_hash_works(self):
        """
        __hash__ returns different hashes for different values.
        """
        assert hash(HashC(1, 2)) != hash(HashC(1, 1))


class TestAddInit(object):
    """
    Tests for `_add_init`.
    """
    def test_init(self):
        """
        If `init` is False, ignore that attribute.
        """
        C = make_class("C", {"a": attr(init=False), "b": attr()})
        with pytest.raises(TypeError) as e:
            C(a=1, b=2)

        msg = e.value if PY26 else e.value.args[0]
        assert "__init__() got an unexpected keyword argument 'a'" == msg

    def test_sets_attributes(self):
        """
        The attributes are initialized using the passed keywords.
        """
        obj = InitC(a=1, b=2)
        assert 1 == obj.a
        assert 2 == obj.b

    def test_default(self):
        """
        If a default value is present, it's used as fallback.
        """
        class C(object):
            __attrs_attrs__ = [
                simple_attr(name="a", default=2),
                simple_attr(name="b", default="hallo"),
                simple_attr(name="c", default=None),
            ]

        C = _add_init(C)
        i = C()
        assert 2 == i.a
        assert "hallo" == i.b
        assert None is i.c

    def test_factory(self):
        """
        If a default factory is present, it's used as fallback.
        """
        class D(object):
            pass

        class C(object):
            __attrs_attrs__ = [
                simple_attr(name="a", default=Factory(list)),
                simple_attr(name="b", default=Factory(D)),
            ]
        C = _add_init(C)
        i = C()
        assert [] == i.a
        assert isinstance(i.b, D)

    def test_validator(self):
        """
        If a validator is passed, call it with the preliminary instance, the
        Attribute, and the argument.
        """
        class VException(Exception):
            pass

        def raiser(*args):
            raise VException(*args)

        C = make_class("C", {"a": attr("a", validator=raiser)})
        with pytest.raises(VException) as e:
            C(42)
        assert (C.a, 42,) == e.value.args[1:]
        assert isinstance(e.value.args[0], C)

    def test_validator_others(self):
        """
        Does not interfere when setting non-attrs attributes.
        """
        C = make_class("C", {"a": attr("a", validator=instance_of(int))})
        i = C(1)
        i.b = "foo"
        assert 1 == i.a
        assert "foo" == i.b

    def test_underscores(self):
        """
        The argument names in `__init__` are without leading and trailing
        underscores.
        """
        class C(object):
            __attrs_attrs__ = [simple_attr("_private")]

        C = _add_init(C)
        i = C(private=42)
        assert 42 == i._private


class TestNothing(object):
    """
    Tests for `_Nothing`.
    """
    def test_copy(self):
        """
        __copy__ returns the same object.
        """
        n = _Nothing()
        assert n is copy.copy(n)

    def test_deepcopy(self):
        """
        __deepcopy__ returns the same object.
        """
        n = _Nothing()
        assert n is copy.deepcopy(n)

    def test_eq(self):
        """
        All instances are equal.
        """
        assert _Nothing() == _Nothing() == NOTHING
        assert not (_Nothing() != _Nothing)
