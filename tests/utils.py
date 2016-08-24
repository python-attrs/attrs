"""
Common helper functions for tests.
"""

from __future__ import absolute_import, division, print_function

import keyword
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

    ~702 different attribute names should be enough in practice.

    Some short strings (such as 'as') are keywords, so we skip them.
    """
    lc = string.ascii_lowercase
    for c in lc:
        yield c
    for outer in lc:
        for inner in lc:
            res = outer + inner
            if keyword.iskeyword(res):
                continue
            yield outer + inner


def _create_hyp_class(attrs):
    """
    A helper function for Hypothesis to generate attrs classes.
    """
    return make_class('HypClass', dict(zip(_gen_attr_names(), attrs)))


def _create_hyp_nested_strategy(simple_class_strategy):
    """
    Create a recursive attrs class.

    Given a strategy for building (simpler) classes, create and return
    a strategy for building classes that have as an attribute: either just
    the simpler class, a list of simpler classes, or a dict mapping the string
    "cls" to a simpler class.
    """
    # Use a tuple strategy to combine simple attributes and an attr class.
    def just_class(tup):
        combined_attrs = list(tup[0])
        combined_attrs.append(attr.ib(default=attr.Factory(tup[1])))
        return _create_hyp_class(combined_attrs)

    def list_of_class(tup):
        default = attr.Factory(lambda: [tup[1]()])
        combined_attrs = list(tup[0])
        combined_attrs.append(attr.ib(default=default))
        return _create_hyp_class(combined_attrs)

    def dict_of_class(tup):
        default = attr.Factory(lambda: {"cls": tup[1]()})
        combined_attrs = list(tup[0])
        combined_attrs.append(attr.ib(default=default))
        return _create_hyp_class(combined_attrs)

    # A strategy producing tuples of the form ([list of attributes], <given
    # class strategy>).
    attrs_and_classes = st.tuples(list_of_attrs, simple_class_strategy)

    return st.one_of(attrs_and_classes.map(just_class),
                     attrs_and_classes.map(list_of_class),
                     attrs_and_classes.map(dict_of_class))

bare_attrs = st.just(attr.ib(default=None))
int_attrs = st.integers().map(lambda i: attr.ib(default=i))
str_attrs = st.text().map(lambda s: attr.ib(default=s))
float_attrs = st.floats().map(lambda f: attr.ib(default=f))
dict_attrs = (st.dictionaries(keys=st.text(), values=st.integers())
              .map(lambda d: attr.ib(default=d)))

simple_attrs = st.one_of(bare_attrs, int_attrs, str_attrs, float_attrs,
                         dict_attrs)

# Python functions support up to 255 arguments.
list_of_attrs = st.lists(simple_attrs, average_size=9, max_size=50)
simple_classes = list_of_attrs.map(_create_hyp_class)

# Ok, so st.recursive works by taking a base strategy (in this case,
# simple_classes) and a special function. This function receives a strategy,
# and returns another strategy (building on top of the base strategy).
nested_classes = st.recursive(simple_classes, _create_hyp_nested_strategy)
