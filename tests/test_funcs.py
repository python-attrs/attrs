# -*- coding: utf-8 -*-

"""
Tests for `attr._funcs`.
"""

from __future__ import absolute_import, division, print_function

import pytest

from attr._funcs import (
    asdict,
    assoc,
    fields,
    has,
    validate,
)
from attr._make import (
    Attribute,
    attr,
    attributes,
    make_class,
)


@attributes
class C(object):
    x = attr()
    y = attr()


class TestFields(object):
    """
    Tests for `fields`.
    """
    def test_instance(self):
        """
        Raises `TypeError` on non-classes.
        """
        with pytest.raises(TypeError) as e:
            fields(C(1, 2))
        assert "Passed object must be a class." == e.value.args[0]

    def test_handler_non_attrs_class(self):
        """
        Raises `ValueError` if passed a non-``attrs`` instance.
        """
        with pytest.raises(ValueError) as e:
            fields(object)
        assert (
            "{o!r} is not an attrs-decorated class.".format(o=object)
        ) == e.value.args[0]

    def test_fields(self):
        """
        Returns a list of `Attribute`a.
        """
        assert all(isinstance(a, Attribute) for a in fields(C))

    def test_copies(self):
        """
        Returns a new list object with new `Attribute` objects.
        """
        assert C.__attrs_attrs__ is not fields(C)
        assert all(new == original and new is not original
                   for new, original
                   in zip(fields(C), C.__attrs_attrs__))


class TestAsDict(object):
    """
    Tests for `asdict`.
    """
    def test_shallow(self):
        """
        Shallow asdict returns correct dict.
        """
        assert {
            "x": 1,
            "y": 2,
        } == asdict(C(x=1, y=2), False)

    def test_recurse(self):
        """
        Deep asdict returns correct dict.
        """
        assert {
            "x": {"x": 1, "y": 2},
            "y": {"x": 3, "y": 4},
        } == asdict(C(
            C(1, 2),
            C(3, 4),
        ))

    def test_filter(self):
        """
        Attributes that are supposed to be skipped are skipped.
        """
        assert {
            "x": {"x": 1},
        } == asdict(C(
            C(1, 2),
            C(3, 4),
        ), filter=lambda a, v: a.name != "y")

    @pytest.mark.parametrize("container", [
        list,
        tuple,
    ])
    def test_lists_tuples(self, container):
        """
        If recurse is True, also recurse into lists.
        """
        assert {
            "x": 1,
            "y": [{"x": 2, "y": 3}, {"x": 4, "y": 5}, "a"],
        } == asdict(C(1, container([C(2, 3), C(4, 5), "a"])))

    def test_dicts(self):
        """
        If recurse is True, also recurse into dicts.
        """
        assert {
            "x": 1,
            "y": {"a": {"x": 4, "y": 5}},
        } == asdict(C(1, {"a": C(4, 5)}))


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


class TestValidate(object):
    """
    Tests for `validate`.
    """
    def test_success(self):
        """
        If the validator suceeds, nothing gets raised.
        """
        C = make_class("C", {"x": attr(validator=lambda _, __: None),
                             "y": attr()})
        validate(C(1, 2))

    def test_propagates(self):
        """
        The exception of the validator is handed through.
        """
        def raiser(_, value):
            if value == 42:
                raise FloatingPointError

        C = make_class("C", {"x": attr(validator=raiser)})
        i = C(1)
        i.x = 42

        with pytest.raises(FloatingPointError):
            validate(i)
