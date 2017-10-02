"""
Tests for PEP-526 type annotations.
"""

from __future__ import absolute_import, division, print_function

import pytest

from attr._make import (
    attrib,
    attrs,
    fields
)

import typing


class TestAnnotations(object):
    """
    Tests for types derived from variable annotations (PEP-526).
    """

    def test_basic_annotations(self):
        """
        Sets the `Attribute.type` attr from basic type annotations.
        """
        @attrs
        class C(object):
            x: int = attrib()
            y = attrib(type=str)
            z = attrib()

        assert int is fields(C).x.type
        assert str is fields(C).y.type
        assert None is fields(C).z.type

    def test_catches_basic_type_conflict(self):
        """
        Raises ValueError type is specified both ways.
        """
        with pytest.raises(ValueError) as e:
            @attrs
            class C:
                x: int = attrib(type=int)

        assert ("Type annotation and type argument cannot "
                "both be present",) == e.value.args

    def test_typing_annotations(self):
        """
        Sets the `Attribute.type` attr from typing annotations.
        """
        @attrs
        class C(object):
            x: typing.List[int] = attrib()
            y = attrib(type=typing.Optional[str])

        assert typing.List[int] is fields(C).x.type
        assert typing.Optional[str] is fields(C).y.type
