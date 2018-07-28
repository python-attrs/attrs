from typing import TypeVar, Optional, Callable
from . import _ConverterType

_T = TypeVar("_T")

def optional(
    converter: _ConverterType[_T]
) -> _ConverterType[Optional[_T]]: ...
def default_if_none(
    default: _T = ..., factory: Callable[[], _T] = ...
) -> _ConverterType[_T]: ...
