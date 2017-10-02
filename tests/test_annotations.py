"""
Tests for PEP-526 type annotations.
"""

from __future__ import absolute_import, division, print_function

import pytest

import attr

import typing


class TestAnnotations(object):
    """
    Tests for types derived from variable annotations (PEP-526).
    """

    def test_basic_annotations(self):
        """
        Sets the `Attribute.type` attr from basic type annotations.
        """
        @attr.s
        class C(object):
            x: int = attr.ib()
            y = attr.ib(type=str)
            z = attr.ib()

        assert int is attr.fields(C).x.type
        assert str is attr.fields(C).y.type
        assert None is attr.fields(C).z.type

    def test_catches_basic_type_conflict(self):
        """
        Raises ValueError type is specified both ways.
        """
        with pytest.raises(ValueError) as e:
            @attr.s
            class C:
                x: int = attr.ib(type=int)

        assert ("Type annotation and type argument cannot "
                "both be present",) == e.value.args

    def test_typing_annotations(self):
        """
        Sets the `Attribute.type` attr from typing annotations.
        """
        @attr.s
        class C(object):
            x: typing.List[int] = attr.ib()
            y = attr.ib(type=typing.Optional[str])

        assert typing.List[int] is attr.fields(C).x.type
        assert typing.Optional[str] is attr.fields(C).y.type
