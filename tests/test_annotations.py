"""
Tests for PEP-526 type annotations.

Python 3.6+ only.
"""

import typing

import pytest

import attr


class TestAnnotations:
    """
    Tests for types derived from variable annotations (PEP-526).
    """

    def test_basic_annotations(self):
        """
        Sets the `Attribute.type` attr from basic type annotations.
        """
        @attr.s
        class C:
            x: int = attr.ib()
            y = attr.ib(type=str)
            z = attr.ib()

        assert int is attr.fields(C).x.type
        assert str is attr.fields(C).y.type
        assert None is attr.fields(C).z.type

    def test_catches_basic_type_conflict(self):
        """
        Raises ValueError if type is specified both ways.
        """
        with pytest.raises(ValueError) as e:
            @attr.s
            class C:
                x: int = attr.ib(type=int)

        assert (
            "Type annotation and type argument cannot both be present",
        ) == e.value.args

    def test_typing_annotations(self):
        """
        Sets the `Attribute.type` attr from typing annotations.
        """
        @attr.s
        class C:
            x: typing.List[int] = attr.ib()
            y = attr.ib(type=typing.Optional[str])

        assert typing.List[int] is attr.fields(C).x.type
        assert typing.Optional[str] is attr.fields(C).y.type

    def test_only_attrs_annotations_collected(self):
        """
        Annotations that aren't set to an attr.ib are ignored.
        """
        @attr.s
        class C:
            x: typing.List[int] = attr.ib()
            y: int

        assert 1 == len(attr.fields(C))

    def test_auto_attribs(self):
        """
        If *auto_attribs* is True, bare annotations are collected too.
        """
        @attr.s(auto_attribs=True)
        class C:
            x: typing.List[int]
            y: int
            z: typing.Any = attr.ib(default=3)

        assert "C(x=1, y=2, z=3)" == repr(C(1, 2))
        assert typing.List[int] == attr.fields(C).x.type
        assert int == attr.fields(C).y.type
        assert typing.Any == attr.fields(C).z.type
