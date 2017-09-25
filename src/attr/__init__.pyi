from typing import Any, Callable, Dict, Generic, Iterable, List, Optional, Mapping, Tuple, Type, TypeVar, Union, overload
from . import exceptions
from . import filters
from . import converters
from . import validators

# typing --

_T = TypeVar('_T')
_C = TypeVar('_C', bound=type)
_M = TypeVar('_M', bound=Mapping)
_TT = TypeVar('_TT', bound=tuple)

ValidatorType = Callable[[object, 'Attribute', Any], Any]
ConverterType = Callable[[Any], Any]
FilterType = Callable[['Attribute', Any], bool]

# _make --

class _CountingAttr: ...

NOTHING : object

class Factory(Generic[_T]):
    factory : Union[Callable[[], _T], Callable[[object], _T]]
    takes_self : bool
    def __init__(self, factory: Union[Callable[[], _T], Callable[[object], _T]], takes_self: bool = ...) -> None: ...

class Attribute:
    __slots__ = ("name", "default", "validator", "repr", "cmp", "hash", "init", "convert", "metadata", "type")
    def __init__(self, name: str, default: Any, validator: Optional[Union[ValidatorType, List[ValidatorType]]], repr: bool, cmp: bool, hash: Optional[bool], init: bool, convert: Optional[ConverterType] = ..., metadata: Mapping = ..., type: Union[type, Factory] = ...) -> None: ...

# NOTE: this overload for `attr` returns Any so that static analysis passes when used in the form:  x : int = attr()
@overload
def attr(default: Any = ..., validator: Optional[Union[ValidatorType, List[ValidatorType]]] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., convert: Optional[ConverterType] = ..., metadata: Mapping = ...) -> Any: ...
@overload
def attr(default: Any = ..., validator: Optional[Union[ValidatorType, List[ValidatorType]]] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., convert: Optional[ConverterType] = ..., metadata: Mapping = ..., type: Union[Type[_T], Factory[_T]] = ...) -> _T: ...

@overload
def attributes(maybe_cls: _C = ..., these: Optional[Dict[str, _CountingAttr]] = ..., repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., slots: bool = ..., frozen: bool = ..., str: bool = ...) -> _C: ...
@overload
def attributes(maybe_cls: None = ..., these: Optional[Dict[str, _CountingAttr]] = ..., repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., slots: bool = ..., frozen: bool = ..., str: bool = ...) -> Callable[[_C], _C]: ...

def fields(cls: type) -> Tuple[Attribute, ...]: ...
def validate(inst: object) -> None: ...

def make_class(name, attrs: Union[List[_CountingAttr], Dict[str, _CountingAttr]], bases: Tuple[type, ...] = ..., **attributes_arguments) -> type: ...

def and_(*validators: Iterable[ValidatorType]) -> ValidatorType: ...

# _funcs --

# FIXME: having problems assigning a default to the factory typevars
def asdict(inst: object, recurse: bool = ..., filter: Optional[FilterType] = ..., dict_factory: Callable[[], _M] = ..., retain_collection_types: bool = ...) -> _M: ...
def astuple(inst: object, recurse: bool = ..., filter: Optional[FilterType] = ..., tuple_factory: Callable[[Iterable], _TT] = ..., retain_collection_types: bool = ...) -> _TT: ...
def has(cls: type) -> bool: ...
def assoc(inst: _T, **changes) -> _T: ...
def evolve(inst: _T, **changes) -> _T: ...

# _config --

def set_run_validators(run: bool) -> None: ...
def get_run_validators() -> bool: ...

# aliases
s = attrs = attributes
ib = attrib = attr
