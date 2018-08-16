from typing import Container, List, Union, TypeVar, Type, Any, Optional, Tuple
from . import _ValidatorType

_T = TypeVar("_T")

def instance_of(
    type: Union[Tuple[Type[_T], ...], Type[_T]]
) -> _ValidatorType[_T]: ...

def provides(interface: Any) -> _ValidatorType[Any]: ...

def optional(
    validator: Union[_ValidatorType[_T], List[_ValidatorType[_T]]]
) -> _ValidatorType[Optional[_T]]: ...

def in_(options: Container[_T]) -> _ValidatorType[_T]: ...

def and_(*validators: _ValidatorType[_T]) -> _ValidatorType[_T]: ...

def deep_iterable(
    member_validator: _ValidatorType[_T],
    iterable_validator: Optional[_ValidatorType[_T]]
) -> _ValidatorType[_T]: ...

def deep_dictionary(
    key_validator: _ValidatorType[_T],
    value_validator: _ValidatorType[_T]
) -> _ValidatorType[_T]: ...

def is_callable() -> _ValidatorType[_T]: ...
