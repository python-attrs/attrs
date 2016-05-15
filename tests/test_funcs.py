"""
Tests for `attr._funcs`.
"""

from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import pytest

from hypothesis import given, strategies as st

from . import simple_classes

from attr._funcs import (
    asdict,
    assoc,
    fields,
    has,
)
from attr._make import (
    attr,
    attributes,
)

MAPPING_TYPES = (dict, OrderedDict)
SEQUENCE_TYPES = (list, tuple)


class TestAsDict(object):
    """
    Tests for `asdict`.
    """
    @given(st.sampled_from(MAPPING_TYPES))
    def test_shallow(self, C, dict_factory):
        """
        Shallow asdict returns correct dict.
        """
        assert {
            "x": 1,
            "y": 2,
        } == asdict(C(x=1, y=2), False, dict_factory=dict_factory)

    @given(st.sampled_from(MAPPING_TYPES))
    def test_recurse(self, C, dict_factory):
        """
        Deep asdict returns correct dict.
        """
        assert {
            "x": {"x": 1, "y": 2},
            "y": {"x": 3, "y": 4},
        } == asdict(C(
            C(1, 2),
            C(3, 4),
        ), dict_factory=dict_factory)

    @given(st.sampled_from(MAPPING_TYPES))
    def test_filter(self, C, dict_factory):
        """
        Attributes that are supposed to be skipped are skipped.
        """
        assert {
            "x": {"x": 1},
        } == asdict(C(
            C(1, 2),
            C(3, 4),
        ), filter=lambda a, v: a.name != "y", dict_factory=dict_factory)

    @given(container=st.sampled_from(SEQUENCE_TYPES))
    def test_lists_tuples(self, container, C):
        """
        If recurse is True, also recurse into lists.
        """
        assert {
            "x": 1,
            "y": [{"x": 2, "y": 3}, {"x": 4, "y": 5}, "a"],
        } == asdict(C(1, container([C(2, 3), C(4, 5), "a"])))

    @given(st.sampled_from(MAPPING_TYPES))
    def test_dicts(self, C, dict_factory):
        """
        If recurse is True, also recurse into dicts.
        """
        res = asdict(C(1, {"a": C(4, 5)}), dict_factory=dict_factory)
        assert {
            "x": 1,
            "y": {"a": {"x": 4, "y": 5}},
        } == res
        assert isinstance(res, dict_factory)

    @given(simple_classes, st.sampled_from(MAPPING_TYPES))
    def test_roundtrip(self, cls, dict_factory):
        """
        Test dumping to dicts and back for Hypothesis-generated classes.
        """
        instance = cls()
        dict_instance = asdict(instance, dict_factory=dict_factory)

        assert isinstance(dict_instance, dict_factory)

        roundtrip_instance = cls(**dict_instance)

        assert instance == roundtrip_instance

    @given(simple_classes)
    def test_asdict_preserve_order(self, cls):
        """
        Field order should be preserved when dumping to OrderedDicts.
        """
        instance = cls()
        dict_instance = asdict(instance, dict_factory=OrderedDict)

        assert [a.name for a in fields(cls)] == list(dict_instance.keys())


class TestHas(object):
    """
    Tests for `has`.
    """
    def test_positive(self, C):
        """
        Returns `True` on decorated classes.
        """
        assert has(C)

    def test_positive_empty(self):
        """
        Returns `True` on decorated classes even if there are no attributes.
        """
        @attributes
        class D(object):
            pass

        assert has(D)

    def test_negative(self):
        """
        Returns `False` on non-decorated classes.
        """
        assert not has(object)


class TestAssoc(object):
    """
    Tests for `assoc`.
    """
    def test_empty(self):
        """
        Empty classes without changes get copied.
        """
        @attributes
        class C(object):
            pass

        i1 = C()
        i2 = assoc(i1)

        assert i1 is not i2
        assert i1 == i2

    def test_no_changes(self, C):
        """
        No changes means a verbatim copy.
        """
        i1 = C(1, 2)
        i2 = assoc(i1)

        assert i1 is not i2
        assert i1 == i2

    def test_change(self, C):
        """
        Changes work.
        """
        i = assoc(C(1, 2), x=42)
        assert C(42, 2) == i

    def test_unknown(self, C):
        """
        Wanting to change an unknown attribute raises a ValueError.
        """
        @attributes
        class C(object):
            x = attr()
            y = 42

        with pytest.raises(ValueError) as e:
            assoc(C(1), y=2)
        assert (
            "y is not an attrs attribute on {cl!r}.".format(cl=C),
        ) == e.value.args
