from __future__ import absolute_import, division, print_function

import pytest
from hypothesis import given
from hypothesis.strategies import booleans

import attr

from attr._compat import TYPE
from attr._make import Attribute, NOTHING


@attr.s
class C1(object):
    x = attr.ib(validator=attr.validators.instance_of(int))
    y = attr.ib()


@attr.s(slots=True)
class C1Slots(object):
    x = attr.ib(validator=attr.validators.instance_of(int))
    y = attr.ib()

foo = None


@attr.s()
class C2(object):
    x = attr.ib(default=foo)
    y = attr.ib(default=attr.Factory(list))


@attr.s(slots=True)
class C2Slots(object):
    x = attr.ib(default=foo)
    y = attr.ib(default=attr.Factory(list))


@attr.s
class Super(object):
    x = attr.ib()

    def meth(self):
        return self.x


@attr.s(slots=True)
class SuperSlots(object):
    x = attr.ib()

    def meth(self):
        return self.x


@attr.s
class Sub(Super):
    y = attr.ib()


@attr.s(slots=True)
class SubSlots(SuperSlots):
    y = attr.ib()


class TestDarkMagic(object):
    """
    Integration tests.
    """
    @pytest.mark.parametrize("cls", [C2, C2Slots])
    def test_fields(self, cls):
        """
        `attr.fields` works.
        """
        assert (
            Attribute(name="x", default=foo, validator=None,
                      repr=True, cmp=True, hash=True, init=True),
            Attribute(name="y", default=attr.Factory(list), validator=None,
                      repr=True, cmp=True, hash=True, init=True),
        ) == attr.fields(cls)

    @pytest.mark.parametrize("cls", [C1, C1Slots])
    def test_asdict(self, cls):
        """
        `attr.asdict` works.
        """
        assert {
            "x": 1,
            "y": 2,
        } == attr.asdict(cls(x=1, y=2))

    @pytest.mark.parametrize("cls", [C1, C1Slots])
    def test_validator(self, cls):
        """
        `instance_of` raises `TypeError` on type mismatch.
        """
        with pytest.raises(TypeError) as e:
            cls("1", 2)

        # Using C1 explicitly, since slot classes don't support this.
        assert (
            "'x' must be <{type} 'int'> (got '1' that is a <{type} "
            "'str'>).".format(type=TYPE),
            C1.x, int, "1",
        ) == e.value.args

    @given(booleans())
    def test_renaming(self, slots):
        """
        Private members are renamed but only in `__init__`.
        """
        @attr.s(slots=slots)
        class C3(object):
            _x = attr.ib()

        assert "C3(_x=1)" == repr(C3(x=1))

    @given(booleans())
    def test_programmatic(self, slots):
        """
        `attr.make_class` works.
        """
        PC = attr.make_class("PC", ["a", "b"], slots=slots)
        assert (
            Attribute(name="a", default=NOTHING, validator=None,
                      repr=True, cmp=True, hash=True, init=True),
            Attribute(name="b", default=NOTHING, validator=None,
                      repr=True, cmp=True, hash=True, init=True),
        ) == attr.fields(PC)

    @pytest.mark.parametrize("cls", [Sub, SubSlots])
    def test_subclassing_with_extra_attrs(self, cls):
        """
        Sub-classing (where the subclass has extra attrs) does what you'd hope
        for.
        """
        obj = object()
        i = cls(x=obj, y=2)
        assert i.x is i.meth() is obj
        assert i.y == 2
        if cls is Sub:
            assert "Sub(x={obj}, y=2)".format(obj=obj) == repr(i)
        else:
            assert "SubSlots(x={obj}, y=2)".format(obj=obj) == repr(i)

    @pytest.mark.parametrize("base", [Super, SuperSlots])
    def test_subclass_without_extra_attrs(self, base):
        """
        Sub-classing (where the subclass does not have extra attrs) still
        behaves the same as a subclss with extra attrs.
        """
        class Sub2(base):
            pass

        obj = object()
        i = Sub2(x=obj)
        assert i.x is i.meth() is obj
        assert "Sub2(x={obj})".format(obj=obj) == repr(i)
