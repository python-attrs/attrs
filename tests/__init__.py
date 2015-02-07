# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from attr import Attribute
from attr._make import NOTHING, make_class


def simple_class(no_cmp=True, no_repr=True, no_hash=True):
    """
    Return a new simple class.
    """
    return make_class(
        "C", ["a", "b"],
        no_cmp=no_cmp, no_repr=no_repr, no_hash=no_hash, no_init=False,
    )


def simple_attr(name, default=NOTHING, validator=None, no_repr=False,
                no_cmp=False, no_hash=False, no_init=False):
    """
    Return an attribute with a name and no other bells and whistles.
    """
    return Attribute(
        name=name, default=default, validator=validator, no_repr=no_repr,
        no_cmp=no_cmp, no_hash=no_hash, no_init=no_init
    )


class TestSimpleClass(object):
    """
    Tests for the testing helper function `make_class`.
    """
    def test_returns_class(self):
        """
        Returns a class object.
        """
        assert type is simple_class().__class__

    def returns_distinct_classes(self):
        """
        Each call returns a completely new class.
        """
        assert simple_class() is not simple_class()
