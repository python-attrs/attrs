# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest

import attr

from attr._make import Attribute, NOTHING

from . import TYPE


@attr.s
class C1(object):
    x = attr.ib(validator=attr.validators.instance_of(int))
    y = attr.ib()


foo = None


@attr.s()
class C2(object):
    x = attr.ib(default_value=foo)
    y = attr.ib(default_factory=list)


class TestDarkMagic(object):
    """
    Integration tests.
    """
    def test_ls(self):
        """
        `attr.ls` works.
        """
        assert [
            Attribute(name="x", default_value=None, default_factory=NOTHING,
                      validator=None),
            Attribute(name="y", default_value=NOTHING, default_factory=list,
                      validator=None),
        ] == attr.ls(C2)

    def test_to_dict(self):
        """
        `attr.to_dict` works.
        """
        assert {
            "x": 1,
            "y": 2,
        } == attr.to_dict(C1(x=1, y=2))

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
