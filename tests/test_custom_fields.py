"""Tests for the custom attributes functionality."""

from __future__ import annotations

from functools import partial
from typing import Generic, TypeVar

from attrs import Attribute, AttrsInstance, define
from attrs.custom_fields import custom_fields


T = TypeVar("T")


@define
class CustomAttribute(Generic[T]):
    """A custom attribute, for tests."""

    cl: type[AttrsInstance]
    name: str
    attribute_type: T

    @classmethod
    def _from_attrs_attribute(
        cls, attrs_cls: type[AttrsInstance], attribute: Attribute[T]
    ):
        return cls(attrs_cls, attribute.name, attribute.type)


cust_fields = partial(custom_fields, attribute_model=CustomAttribute)
cust_resolved_fields = partial(
    custom_fields, attribute_model=CustomAttribute, resolve_types=True
)


def test_simple_custom_fields():
    """Simple custom attribute overriding works."""

    @define
    class Test:
        a: int
        b: float

    for _ in range(2):
        # Do it twice to test caching.
        f = cust_fields(Test)

        assert isinstance(f.a, CustomAttribute)
        assert isinstance(f.b, CustomAttribute)

        assert not hasattr(f, "c")

        assert f.a.name == "a"
        assert f.a.cl is Test
        assert f.a.attribute_type == "int"


def test_resolved_custom_fields():
    """Resolved custom attributes work."""

    @define
    class Test:
        a: int
        b: float

    for _ in range(2):
        # Do it twice to test caching.
        f = cust_resolved_fields(Test)

        assert isinstance(f.a, CustomAttribute)
        assert isinstance(f.b, CustomAttribute)

        assert not hasattr(f, "c")

        assert f.a.name == "a"
        assert f.a.cl is Test
        assert f.a.attribute_type is int
