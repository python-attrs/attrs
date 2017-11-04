from typing import Any, Callable, Dict, Generic, Iterable, List, Optional, Mapping, Tuple, Type, TypeVar, Union, overload
# `import X as X` is required to expose these to mypy. otherwise they are invisible
from . import exceptions as exceptions
from . import filters as filters
from . import converters as converters
from . import validators as validators

# typing --

_T = TypeVar('_T')
_C = TypeVar('_C', bound=type)
_M = TypeVar('_M', bound=Mapping)
_I = TypeVar('_I', bound=Iterable)

_ValidatorType = Callable[[Any, 'Attribute', Any], Any]
# FIXME: Bind to attribute type?
_ConverterType = Callable[[Any], Any]
_FilterType = Callable[['Attribute', Any], bool]

# _make --

class _CountingAttr:
    def __init__(self, default: Any = ..., validator: Optional[Union[_ValidatorType, List[_ValidatorType], Tuple[_ValidatorType, ...]]] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., convert: Optional[_ConverterType] = ..., metadata: Mapping = ..., type: type = ...) -> None: ...

NOTHING : object

class Factory(Generic[_T]):
    factory : Union[Callable[[], _T], Callable[[Any], _T]]
    takes_self : bool
    def __init__(self, factory: Union[Callable[[], _T], Callable[[Any], _T]], takes_self: bool = ...) -> None: ...

class Attribute:
    __slots__ = ("name", "default", "validator", "repr", "cmp", "hash", "init", "convert", "metadata", "type")
    name: str
    default: Any
    validator: Optional[Union[_ValidatorType, List[_ValidatorType], Tuple[_ValidatorType, ...]]]
    repr: bool
    cmp: bool
    hash: Optional[bool]
    init: bool
    convert: Optional[_ConverterType]
    metadata: Mapping
    type: Any

# NOTE: this overload for `attr` returns Any so that static analysis passes when used in the form:  x : int = attr()
@overload
def attr(default: Any = ..., validator: Optional[Union[_ValidatorType, List[_ValidatorType], Tuple[_ValidatorType, ...]]] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., convert: Optional[_ConverterType] = ..., metadata: Mapping = ...) -> Any: ...
@overload
def attr(default: Any = ..., validator: Optional[Union[_ValidatorType, List[_ValidatorType], Tuple[_ValidatorType, ...]]] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., convert: Optional[_ConverterType] = ..., metadata: Mapping = ..., type: Type[_T] = ...) -> _T: ...

@overload
def attributes(maybe_cls: _C = ..., these: Optional[Dict[str, _CountingAttr]] = ..., repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., slots: bool = ..., frozen: bool = ..., str: bool = ...) -> _C: ...
@overload
def attributes(maybe_cls: None = ..., these: Optional[Dict[str, _CountingAttr]] = ..., repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., slots: bool = ..., frozen: bool = ..., str: bool = ...) -> Callable[[_C], _C]: ...

def fields(cls: type) -> Tuple[Attribute, ...]: ...
def validate(inst: Any) -> None: ...

def make_class(name, attrs: Union[List[_CountingAttr], Dict[str, _CountingAttr]], bases: Tuple[type, ...] = ..., **attributes_arguments) -> type: ...

# _funcs --

# FIXME: having problems assigning a default to the factory typevars
# def asdict(inst: Any, recurse: bool = ..., filter: Optional[_FilterType] = ..., dict_factory: Type[_M] = dict, retain_collection_types: bool = ...) -> _M[str, Any]: ...
# def astuple(inst: Any, recurse: bool = ..., filter: Optional[_FilterType] = ..., tuple_factory: Type[_I] = tuple, retain_collection_types: bool = ...) -> _I: ...
def asdict(inst: Any, recurse: bool = ..., filter: Optional[_FilterType] = ..., dict_factory: Type[_M] = ..., retain_collection_types: bool = ...) -> _M: ...
def astuple(inst: Any, recurse: bool = ..., filter: Optional[_FilterType] = ..., tuple_factory: Type[_I] = ..., retain_collection_types: bool = ...) -> _I: ...
def has(cls: type) -> bool: ...
def assoc(inst: _T, **changes) -> _T: ...
def evolve(inst: _T, **changes) -> _T: ...

# _config --

def set_run_validators(run: bool) -> None: ...
def get_run_validators() -> bool: ...

# aliases
s = attrs = attributes
ib = attrib = attr
