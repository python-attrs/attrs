# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest

from attr._make import Attribute
from attr._dunders import (
    NOTHING,
    _add_cmp,
    _add_hash,
    _add_init,
    _add_repr,
)


def simple_attr(name):
    """
    Return an attribute with a name and no other bells and whistles.
    """
    return Attribute(name=name, default_value=NOTHING, default_factory=NOTHING,
                     validator=None)


def make_class():
    """
    Return a new simple class.
    """
    class C(object):
        __attrs_attrs__ = [simple_attr("a"), simple_attr("b")]

        def __init__(self, a, b):
            self.a = a
            self.b = b
    return C

CmpC = _add_cmp(make_class())
ReprC = _add_repr(make_class())
HashC = _add_hash(make_class())


class InitC(object):
    __attrs_attrs__ = [simple_attr("a"), simple_attr("b")]

InitC = _add_init(InitC)


class TestMakeClass(object):
    """
    Tests for the testing helper function `make_class`.
    """
    def test_returns_class(self):
        """
        Returns a class object.
        """
        assert type is make_class().__class__

    def returns_distinct_classes(self):
        """
        Each call returns a completely new class.
        """
        assert make_class() is not make_class()


class TestAddCmp(object):
    """
    Tests for `_add_cmp`.
    """
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
        Test repr returns a sensible value.
        """
        assert "C(a=1, b=2)" == repr(ReprC(1, 2))


class TestAddHash(object):
    """
    Tests for `_add_hash`.
    """
    def test_hash(self):
        """
        __hash__ returns different hashes for different values.
        """
        assert hash(HashC(1, 2)) != hash(HashC(1, 1))


class TestAddInit(object):
    """
    Tests for `_add_init`.
    """
    def test_sets_attributes(self):
        """
        The attributes are initialized using the passed keywords.
        """
        obj = InitC(a=1, b=2)
        assert 1 == obj.a
        assert 2 == obj.b

    def test_default_value(self):
        """
        If a default value is present, it's used as fallback.
        """
        class C(object):
            __attrs_attrs__ = [
                Attribute("a",
                          default_value=2,
                          default_factory=NOTHING,
                          validator=None,),
                Attribute("b",
                          default_value="hallo",
                          default_factory=NOTHING,
                          validator=None,),
                Attribute("c",
                          default_value=None,
                          default_factory=NOTHING,
                          validator=None,),
            ]

        C = _add_init(C)
        i = C()
        assert 2 == i.a
        assert "hallo" == i.b
        assert None is i.c

    def test_default_factory(self):
        """
        If a default factory is present, it's used as fallback.
        """
        class D(object):
            pass

        class C(object):
            __attrs_attrs__ = [
                Attribute("a",
                          default_value=NOTHING,
                          default_factory=list,
                          validator=None,),
                Attribute("b",
                          default_value=NOTHING,
                          default_factory=D,
                          validator=None,)
            ]
        C = _add_init(C)
        i = C()
        assert [] == i.a
        assert isinstance(i.b, D)

    def test_validator(self):
        """
        If a validator is passed, call it on the argument.
        """
        class VException(Exception):
            pass

        def raiser(arg):
            raise VException(arg)

        class C(object):
            __attrs_attrs__ = [
                Attribute("a",
                          default_value=NOTHING,
                          default_factory=NOTHING,
                          validator=raiser),
            ]
        C = _add_init(C)

        with pytest.raises(VException) as e:
            C(42)
        assert (42,) == e.value.args
