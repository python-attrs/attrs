# -*- coding: utf-8 -*-

"""
Tests for `attr._funcs`.
"""

from __future__ import absolute_import, division, print_function

import pytest

from attr._funcs import (
    assoc,
    has,
    ls,
    to_dict,
)
from attr._make import (
    Attribute,
    attr,
    attributes,
)


@attributes
class C(object):
    x = attr()
    y = attr()


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

    def test_copies(self):
        """
        Returns a new list object with new `Attribute` objects.
        """
        assert C.__attrs_attrs__ is not ls(C)
        assert all(new == original and new is not original
                   for new, original
                   in zip(ls(C), C.__attrs_attrs__))


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

    def test_no_changes(self):
        """
        No changes means a verbatim copy.
        """
        i1 = C(1, 2)
        i2 = assoc(i1)

        assert i1 is not i2
        assert i1 == i2

    def test_change(self):
        """
        Changes work.
        """
        i = assoc(C(1, 2), x=42)
        assert C(42, 2) == i

    def test_unknown(self):
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
