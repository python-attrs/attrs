"""
Tests for python 3 type annotations.
"""

from __future__ import absolute_import, division, print_function

import pytest

from attr._make import (
    attr,
    attributes,
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
        @attributes
        class C(object):
            x: int = attr()
            y = attr(type=str)
            z = attr()
        assert int is C.__attrs_attrs__[0].type
        assert str is C.__attrs_attrs__[1].type
        assert None is C.__attrs_attrs__[2].type

    def test_catches_basic_type_conflict(self):
        """
        Raises ValueError if types conflict.
        """
        with pytest.raises(ValueError) as e:
            @attributes
            class C:
                x: int = attr(type=str)
        assert ("Type conflict: annotated type and given type differ: "
                "<class 'int'> is not <class 'str'>.",) == e.value.args

    def test_typing_annotations(self):
        """
        Sets the `Attribute.type` attr from typing annotations.
        """
        @attributes
        class C(object):
            x: typing.List[int] = attr()
            y = attr(type=typing.Optional[str])

        assert typing.List[int] is C.__attrs_attrs__[0].type
        assert typing.Optional[str] is C.__attrs_attrs__[1].type

    def test_catches_typing_type_conflict(self):
        """
        Raises ValueError if types conflict.
        """
        with pytest.raises(ValueError) as e:
            @attributes
            class C:
                x: int = attr(type=typing.List[str])
        assert ("Type conflict: annotated type and given type differ: "
                "<class 'int'> is not typing.List[str].",) == e.value.args
