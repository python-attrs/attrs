from typing import (
    Container,
    List,
    Union,
    TypeVar,
    Type,
    Any,
    Optional,
    Tuple,
    Iterable,
    Mapping,
    Callable,
)
from . import _ValidatorType

_T = TypeVar("_T")
_I = TypeVar("_I", bound=Iterable[_T])
_K = TypeVar("_K")
_V = TypeVar("_V")
_M = TypeVar("_V", bound=Mapping[_K, _V])

def instance_of(
    type: Union[Tuple[Type[_T], ...], Type[_T]]
) -> _ValidatorType[_T]: ...
def provides(interface: Any) -> _ValidatorType[Any]: ...
def optional(
    validator: Union[_ValidatorType[_T], List[_ValidatorType[_T]]]
) -> _ValidatorType[Optional[_T]]: ...
def in_(options: Container[_T]) -> _ValidatorType[_T]: ...
def and_(*validators: _ValidatorType[_T]) -> _ValidatorType[_T]: ...
def matches_re(
    regex: str,
    flags: int = ...,
    func: Optional[Callable[[str, str, int], ...]] = ...,
): ...
def deep_iterable(
    member_validator: _ValidatorType[_T],
    iterable_validator: Optional[_ValidatorType[_I]] = ...,
) -> _ValidatorType[_I]: ...
def deep_mapping(
    key_validator: _ValidatorType[_K],
    value_validator: _ValidatorType[_V],
    mapping_validator: Optional[_ValidatorType[_M]] = ...,
) -> _ValidatorType[_M]: ...
def is_callable() -> _ValidatorType[_T]: ...
