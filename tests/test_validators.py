# -*- coding: utf-8 -*-

"""
Tests for `attr.validators`.
"""

from __future__ import absolute_import, division, print_function

import pytest

from attr.validators import instance_of
from . import simple_attr, TYPE


class TestInstanceOf(object):
    """
    Tests for `instance_of`.
    """
    def test_success(self):
        """
        Nothing happens if types match.
        """
        v = instance_of(int)
        v(simple_attr("test"), 42)

    def test_subclass(self):
        """
        Subclasses are accepted too.
        """
        v = instance_of(int)
        v(simple_attr("test"), True)  # yep, bools are a subclass of int :(

    def test_fail(self):
        """
        Raises `TypeError` on wrong types.
        """
        v = instance_of(int)
        a = simple_attr("test")
        with pytest.raises(TypeError) as e:
            v(a, "42")
        assert (
            "'test' must be <{type} 'int'> (got '42' that is a <{type} "
            "'str'>).".format(type=TYPE),
            a, int, "42",

        ) == e.value.args

    def test_repr(self):
        """
        Returned validator has a useful `__repr__`.
        """
        v = instance_of(int)
        assert (
            "<instance_of validator for type <{type} 'int'>>"
            .format(type=TYPE)
        ) == repr(v)
