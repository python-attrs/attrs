from __future__ import absolute_import, division, print_function

import pytest

import attr

from attr._compat import TYPE
from attr._make import Attribute, NOTHING


@attr.s
class C1(object):
    x = attr.ib(validator=attr.validators.instance_of(int))
    y = attr.ib()


foo = None


@attr.s()
class C2(object):
    x = attr.ib(default=foo)
    y = attr.ib(default=attr.Factory(list))


@attr.s
class Super(object):
    x = attr.ib()

    def meth(self):
        return self.x


@attr.s
class Sub(Super):
    y = attr.ib()


class TestDarkMagic(object):
    """
    Integration tests.
    """
    def test_fields(self):
        """
        `attr.fields` works.
        """
        assert (
            Attribute(name="x", default=foo, validator=None,
                      repr=True, cmp=True, hash=True, init=True),
            Attribute(name="y", default=attr.Factory(list), validator=None,
                      repr=True, cmp=True, hash=True, init=True),
        ) == attr.fields(C2)

    def test_asdict(self):
        """
        `attr.asdict` works.
        """
        assert {
            "x": 1,
            "y": 2,
        } == attr.asdict(C1(x=1, y=2))

    def test_validator(self):
        """
        `instance_of` raises `TypeError` on type mismatch.
        """
        with pytest.raises(TypeError) as e:
            C1("1", 2)
        assert (
            "'x' must be <{type} 'int'> (got '1' that is a <{type} "
            "'str'>).".format(type=TYPE),
            C1.x, int, "1",
        ) == e.value.args

    def test_renaming(self):
        """
        Private members are renamed but only in `__init__`.
        """
        @attr.s
        class C3(object):
            _x = attr.ib()

        assert "C3(_x=1)" == repr(C3(x=1))

    def test_programmatic(self):
        """
        `attr.make_class` works.
        """
        PC = attr.make_class("PC", ["a", "b"])
        assert (
            Attribute(name="a", default=NOTHING, validator=None,
                      repr=True, cmp=True, hash=True, init=True),
            Attribute(name="b", default=NOTHING, validator=None,
                      repr=True, cmp=True, hash=True, init=True),
        ) == attr.fields(PC)

    def test_subclassing(self):
        """
        Sub-classing does what you'd hope for.
        """
        obj = object()
        i = Sub(x=obj, y=2)
        assert i.x is i.meth() is obj
        assert i.y == 2
        assert "Sub(x={obj}, y=2)".format(obj=obj) == repr(i)
