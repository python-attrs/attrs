from typing import Any, Callable, Dict, Iterable, List, Optional, Mapping, Tuple, Type, TypeVar, Union, overload
from . import exceptions
from . import filters
from . import converters
from . import validators

# typing --

C = TypeVar('C', bound=type)
M = TypeVar('M', bound=Mapping)
T = TypeVar('T', bound=tuple)
I = TypeVar('I')

ValidatorType = Callable[[object, 'Attribute', Any], Any]
ConverterType = Callable[[Any], Any]
FilterType = Callable[['Attribute', Any], bool]

# _make --

class _CountingAttr: ...

NOTHING : object

class Attribute:
    __slots__ = (
        "name", "default", "validator", "repr", "cmp", "hash", "init",
        "convert", "metadata",
    )
    def __init__(self, name: str, default: Any, validator: Optional[Union[ValidatorType, List[ValidatorType]]], repr: bool, cmp: bool, hash: Optional[bool], init: bool, convert: Optional[ConverterType] = ..., metadata: Mapping = ...) -> None: ...

# NOTE: the stub for `attr` returns Any so that static analysis passes when used in the form:  x : int = attr()
def attr(default: Any = ..., validator: Optional[Union[ValidatorType, List[ValidatorType]]] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., convert: Optional[ConverterType] = ..., metadata: Mapping = ...) -> Any: ...

@overload
def attributes(maybe_cls: C = ..., these: Optional[Dict[str, _CountingAttr]] = ..., repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., slots: bool = ..., frozen: bool = ..., str: bool = ...) -> C: ...
@overload
def attributes(maybe_cls: None = ..., these: Optional[Dict[str, _CountingAttr]] = ..., repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., slots: bool = ..., frozen: bool = ..., str: bool = ...) -> Callable[[C], C]: ...

def fields(cls: type) -> Tuple[Attribute, ...]: ...
def validate(inst: object) -> None: ...

class Factory:
    factory : Union[Callable[[Any], Any], Callable[[object, Any], Any]]
    takes_self : bool
    def __init__(self, factory: Union[Callable[[Any], Any], Callable[[object, Any], Any]], takes_self: bool = ...) -> None: ...

def make_class(name, attrs: Union[List[_CountingAttr], Dict[str, _CountingAttr]], bases: Tuple[type, ...] = ..., **attributes_arguments) -> type: ...

def and_(*validators: Iterable[ValidatorType]) -> ValidatorType: ...

# _funcs --

# FIXME: having problems assigning a default to the factory typevars
def asdict(inst: object, recurse: bool = ..., filter: Optional[FilterType] = ..., dict_factory: Callable[[], M] = ..., retain_collection_types: bool = ...) -> M: ...
def astuple(inst: object, recurse: bool = ..., filter: Optional[FilterType] = ..., tuple_factory: Callable[[Iterable], T] = ..., retain_collection_types: bool = ...) -> T: ...
def has(cls: type) -> bool: ...
def assoc(inst: I, **changes) -> I: ...
def evolve(inst: I, **changes) -> I: ...

# _config --

def set_run_validators(run: bool) -> None: ...
def get_run_validators() -> bool: ...

# aliases
s = attrs = attributes
ib = attrib = attr
