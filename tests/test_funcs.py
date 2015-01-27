# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest

from attr._funcs import ls, to_dict
from attr._make import (
    Attribute,
    _make_attr,
    s,
)


@s
class C(object):
    x = _make_attr()
    y = _make_attr()


class TestLs(object):
    def test_instance(self):
        """
        Works also on instances of classes.
        """
        assert ls(C) == ls(C(1, 2))

    def test_handler_non_attrs_class(self):
        """
        Raises `TypeError` if passed a non-attrs instance.
        """
        with pytest.raises(TypeError) as e:
            ls(object)
        assert (
            "{o!r} is not an attrs-decorated class.".format(o=object)
        ) == e.value.args[0]

    def test_ls(self):
        """
        Returns a list of `Attribute`.
        """

        assert all(isinstance(a, Attribute) for a in ls(C))


class TestToDict(object):
    def test_shallow(self):
        """
        Shallow to_dict returns correct dict.
        """
        assert {
            "x": 1,
            "y": 2,
        } == to_dict(C(x=1, y=2), False)

    def test_recurse(self):
        """
        Deep to_dict returns correct dict.
        """
        assert {
            "x": {"x": 1, "y": 2},
            "y": {"x": 3, "y": 4},
        } == to_dict(C(
            C(1, 2),
            C(3, 4),
        ))
