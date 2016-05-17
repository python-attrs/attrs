from __future__ import absolute_import, division, print_function

import string

from hypothesis import strategies as st

import attr
from attr import Attribute
from attr._make import NOTHING, make_class


def simple_class(cmp=False, repr=False, hash=False, slots=False):
    """
    Return a new simple class.
    """
    return make_class(
        "C", ["a", "b"],
        cmp=cmp, repr=repr, hash=hash, init=True, slots=slots
    )


def simple_attr(name, default=NOTHING, validator=None, repr=True,
                cmp=True, hash=True, init=True):
    """
    Return an attribute with a name and no other bells and whistles.
    """
    return Attribute(
        name=name, default=default, validator=validator, repr=repr,
        cmp=cmp, hash=hash, init=init
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


def _gen_attr_names():
    """
    Generate names for attributes, 'a'...'z', then 'aa'...'zz'.

    702 different attribute names should be enough in practice.
    """
    lc = string.ascii_lowercase
    for c in lc:
        yield c
    for outer in lc:
        for inner in lc:
            yield outer + inner


def _create_hyp_class(attrs):
    """
    A helper function for Hypothesis to generate attrs classes.
    """
    return make_class('HypClass', dict(zip(_gen_attr_names(), attrs)))

bare_attrs = st.just(attr.ib(default=None))
int_attrs = st.integers().map(lambda i: attr.ib(default=i))
str_attrs = st.text().map(lambda s: attr.ib(default=s))
float_attrs = st.floats().map(lambda f: attr.ib(default=f))

simple_attrs = st.one_of(bare_attrs, int_attrs, str_attrs, float_attrs)

simple_classes = st.lists(simple_attrs).map(_create_hyp_class)
