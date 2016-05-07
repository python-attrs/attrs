from __future__ import absolute_import, division, print_function

import string

from hypothesis import strategies as st

from attr import Attribute, ib
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


def create_class(attrs):
    # What if we get more than len(string.ascii_lowercase) attributes?
    return make_class('HypClass', dict(zip(string.ascii_lowercase, attrs)))

bare_attrs = st.just(ib(default=None))
int_attrs = st.integers().map(lambda i: ib(default=i))
str_attrs = st.text().map(lambda s: ib(default=s))
float_attrs = st.floats().map(lambda f: ib(default=f))

simple_attrs = st.one_of(bare_attrs, int_attrs, str_attrs, float_attrs)

simple_classes = st.lists(simple_attrs).map(create_class)
