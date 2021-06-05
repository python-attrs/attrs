from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Callable,
    Collection,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from . import _ConverterType


_T = TypeVar("_T")

def pipe(*validators: _ConverterType) -> _ConverterType: ...
def optional(converter: _ConverterType) -> _ConverterType: ...
@overload
def default_if_none(default: _T) -> _ConverterType: ...
@overload
def default_if_none(*, factory: Callable[[], _T]) -> _ConverterType: ...

def to_attrs(cls: Type[_T]) -> Callable[[Union[_T, dict]], _T]: ...

def to_dt(val: Union[datetime, str]) -> datetime: ...

def to_bool(val: Union[bool, int, str]) -> bool: ...

_E = TypeVar("_E", bound=Enum)
def to_enum(cls: Type[_E]) -> Callable[[Union[_E, Any]], _E]: ...

# This is currently not  expressible:
# cls: Type[_ITER]
# converter: Callable[[Any], _T]
# return: _ITER[_T]
_ITER = TypeVar("_ITER", bound=Iterable)
def to_iterable(
    cls: Type[_ITER], converter: Callable[[Any], _T]
) -> Callable[[Iterable], _ITER]: ...

# This is currently not expressible:
# cls: Type[_TUPEL]
# converters: List[Callable[[Any], T1], Callable[[Any], T2], ...]
# return: Callable[[Collection], _TUPEL[T1, T2, ...]
_TUPLE = TypeVar("_TUPLE", bound=Tuple)

def to_tuple(
    cls: Type[_TUPLE], converters: List[Callable[[Any], _T]]
) -> _TUPLE: ...

_MAP = TypeVar("_MAP", bound=Mapping)
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

# This is currently not expressible:
# cls: Type[_MAP]
# key_converter: Callable[[Any], _KT],
# val_converter: Callable[[Any], _VT],
# return: _MAP[_KT, _VT]
def to_mapping(
    cls: Type[_MAP],
    key_converter: Callable[[Any], _KT],
    val_converter: Callable[[Any], _VT],
) -> _MAP: ...

# This is currently not expressible:
# converter: List[Callable[[Any], _T1], Callable[[Any], _T2], ...]
# return: Callable[[Any], Union[T1, T2, ...]]
def to_union(
    converters: List[Callable[[Any], Any]]
) -> Callable[[Any], Any]: ...
