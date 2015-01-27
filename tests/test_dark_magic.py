# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


import attr

from attr._make import Attribute, NOTHING


@attr.s
class C1(object):
    x = attr.a()
    y = attr.a()


foo = None


@attr.s()
class C2(object):
    x = attr.a(default_value=foo)
    y = attr.a(default_factory=list)


class TestDarkMagic(object):
    """
    Integration tests.
    """
    def test_ls(self):
        """
        `attr.ls` works.
        """
        assert [
            Attribute(name="x", default_value=None, default_factory=NOTHING),
            Attribute(name="y", default_value=NOTHING, default_factory=list),
        ] == attr.ls(C2)

    def test_to_dict(self):
        """
        `attr.to_dict` works.
        """
        assert {
            "x": 1,
            "y": 2,
        } == attr.to_dict(C1(x=1, y=2))
