# SPDX-License-Identifier: MIT

"""
Tests for types with dataclass compatibility added.
"""

import dataclasses

from typing import Annotated, Any

import pytest

import attrs


def _fields_as_tuple(o: Any) -> list[tuple[object, ...]]:
    return [
        (
            f._field_type,
            f.name,
            f.type,
            f.kw_only,
            f.metadata,
            f.default,
            f.default_factory,
        )
        for f in dataclasses.fields(o)
    ]


class TestDataclassCompatible:
    """
    Tests for types with dataclass compatibility added.
    """

    def test_dataclass_compatible_fields(self):
        """
        Check that setting `dataclass_compatible` makes a dataclass-y type.
        """

        @attrs.define(dataclass_compatible=True)
        class C:
            x: Annotated[int, "some-annotation"]
            y: "float" = 3.14
            z: str = attrs.field(metadata={"foo": "bar"}, default="baz")
            my_list: list[int] = attrs.field(factory=list)

            def __attrs_post_init__(self) -> None:
                self.x += 1

        @dataclasses.dataclass
        class D:
            x: Annotated[int, "some-annotation"]
            y: "float" = 3.14
            z: str = dataclasses.field(metadata={"foo": "bar"}, default="baz")
            my_list: list[int] = dataclasses.field(default_factory=list)

            def __post_init__(self) -> None:
                self.x += 1

        # Assert at the class level
        assert _fields_as_tuple(C) == _fields_as_tuple(D)

        # Assert at the instance level
        assert _fields_as_tuple(C(1)) == _fields_as_tuple(D(1))

        # Check high level dataclasses functions
        assert dataclasses.is_dataclass(C) == dataclasses.is_dataclass(D)
        assert dataclasses.is_dataclass(C(1)) == dataclasses.is_dataclass(D(1))
        assert dataclasses.asdict(C(1)) == dataclasses.asdict(D(1))
        assert dataclasses.astuple(C(1)) == dataclasses.astuple(D(1))
        assert dataclasses.asdict(
            dataclasses.replace(C(1), x=2)
        ) == dataclasses.asdict(dataclasses.replace(D(1), x=2))

    def test_raises_on_missing_type(self):
        """
        Raises ValueError if type is missing.
        """
        with pytest.raises(ValueError) as e:

            @attrs.define(dataclass_compatible=True)
            class C:
                x = attrs.field()

        assert (
            "__dataclass_fields__ can only be generated if all attributes are annotated.",
        ) == e.value.args
