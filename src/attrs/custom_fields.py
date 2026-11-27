from __future__ import annotations

from typing import Protocol, TypeVar

from attr._make import _make_attr_tuple_class
from attrs import Attribute, AttrsInstance, fields
from attrs import resolve_types as _resolve_types


__all__ = ["custom_fields"]

T = TypeVar("T")


class AttributeModel(Protocol[T]):
    """Custom attributes must conform to this."""

    @classmethod
    def _from_attrs_attribute(
        cls: type[AttributeModel],
        cl: type[AttrsInstance],
        attribute: Attribute[T],
    ) -> AttributeModel[T]:
        """Create a custom attribute model from an `attrs.Attribute`."""
        ...


def custom_fields(
    cls: type[AttrsInstance],
    attribute_model: type[AttributeModel],
    resolve_types: bool = False,
):
    """
    Return the attrs fields tuple for cls with the provided attribute model.

    Args:
        cls: Class to introspect.
        attribute_model: The attribute model to use.
        resolve_types: Whether to resolve the class types first.

    Raises:
        TypeError: If *cls* is not a class.
        attrs.exceptions.NotAnAttrsClassError: If *cls* is not an *attrs*
            class.

    Returns:
        tuple (with name accessors) of `attribute_model`.

    .. versionadded:: 25.1.0
    """
    attrs = getattr(cls, f"__attrs_{id(attribute_model)}__", None)

    if attrs is None:
        if resolve_types:
            _resolve_types(cls)
        base_attrs = fields(cls)
        AttrsClass = _make_attr_tuple_class(
            cls.__name__, [a.name for a in base_attrs]
        )
        attrs = AttrsClass(
            attribute_model._from_attrs_attribute(cls, a) for a in base_attrs
        )
        setattr(cls, f"__attrs_{id(attribute_model)}__", attrs)

    return attrs
