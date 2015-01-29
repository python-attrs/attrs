# -*- coding: utf-8 -*-

"""
Tests for `attr._funcs`.
"""

from __future__ import absolute_import, division, print_function

import pytest

from attr._funcs import ls, has, to_dict
from attr._make import (
    Attribute,
    _make_attr,
    _add_methods,
)


@_add_methods
class C(object):
    x = _make_attr()
    y = _make_attr()


class TestLs(object):
    """
    Tests for `ls`.
    """
    def test_instance(self):
        """
        Raises `TypeError` on non-classes.
        """
        with pytest.raises(TypeError) as e:
            ls(C(1, 2))
        assert "Passed object must be a class." == e.value.args[0]

    def test_handler_non_attrs_class(self):
        """
        Raises `ValueError` if passed a non-``attrs`` instance.
        """
        with pytest.raises(ValueError) as e:
            ls(object)
        assert (
            "{o!r} is not an attrs-decorated class.".format(o=object)
        ) == e.value.args[0]

    def test_ls(self):
        """
        Returns a list of `Attribute`a.
        """
        assert all(isinstance(a, Attribute) for a in ls(C))


class TestToDict(object):
    """
    Tests for `to_dict`.
    """
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


class TestHas(object):
    """
    Tests for `has`.
    """
    def test_positive(self):
        """
        Returns `True` on decorated classes.
        """
        assert has(C)

    def test_positive_empty(self):
        """
        Returns `True` on decorated classes even if there are no attributes.
        """
        @_add_methods
        class D(object):
            pass

        assert has(D)

    def test_negative(self):
        """
        Returns `False` on non-decorated classes.
        """
        assert not has(object)
