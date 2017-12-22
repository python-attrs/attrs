from typing import Any, Callable, Dict, Generic, List, Optional, Sequence, Mapping, Tuple, Type, TypeVar, Union, overload
# `import X as X` is required to expose these to mypy. otherwise they are invisible
from . import exceptions as exceptions
from . import filters as filters
from . import converters as converters
from . import validators as validators

# typing --

_T = TypeVar('_T')
_C = TypeVar('_C', bound=type)

_ValidatorType = Callable[[Any, 'Attribute', _T], Any]
_ConverterType = Callable[[Any], _T]
_FilterType = Callable[['Attribute', Any], bool]
_ValidatorArgType = Union[_ValidatorType[_T], List[_ValidatorType[_T]], Tuple[_ValidatorType[_T], ...]]

# _make --

NOTHING : object

# Factory lies about its return type to make this possible: `x: List[int] = Factory(list)`
def Factory(factory: Union[Callable[[], _T], Callable[[Any], _T]], takes_self: bool = ...) -> _T: ...

class Attribute(Generic[_T]):
    name: str
    default: Optional[_T]
    validator: Optional[_ValidatorArgType[_T]]
    repr: bool
    cmp: bool
    hash: Optional[bool]
    init: bool
    convert: Optional[_ConverterType[_T]]
    metadata: Dict[Any, Any]
    type: Optional[Type[_T]]

    def __lt__(self, x: Attribute) -> bool: ...
    def __le__(self, x: Attribute) -> bool: ...
    def __gt__(self, x: Attribute) -> bool: ...
    def __ge__(self, x: Attribute) -> bool: ...


# `attr` also lies about its return type to make the following possible:
#     attr()    -> Any
#     attr(8)   -> int
#     attr(validator=<some callable>)  -> Whatever the callable expects.
# This makes this type of assignments possible:
#     x: int = attr(8)
#
# 1st form catches a default value set.  Can't use = ... or you get "overloaded overlap" error.
@overload
def attrib(default: _T, validator: Optional[_ValidatorArgType[_T]] = ...,
           repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ...,
           convert: _ConverterType[_T] = ..., metadata: Mapping = ...,
           type: Type[_T] = ...) -> _T: ...
@overload
def attrib(default: None = ..., validator: Optional[_ValidatorArgType[_T]] = ...,
           repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ...,
           convert: Optional[_ConverterType[_T]] = ..., metadata: Mapping = ...,
           type: Optional[Type[_T]] = ...) -> _T: ...
# 3rd form catches nothing set. So returns Any.
@overload
def attrib(default: None = ..., validator: None = ...,
           repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ...,
           convert: None = ..., metadata: Mapping = ...,
           type: None = ...) -> Any: ...


@overload
def attrs(maybe_cls: _C, these: Optional[Dict[str, Any]] = ..., repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., slots: bool = ..., frozen: bool = ..., str: bool = ...) -> _C: ...
@overload
def attrs(maybe_cls: None = ..., these: Optional[Dict[str, Any]] = ..., repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ..., slots: bool = ..., frozen: bool = ..., str: bool = ...) -> Callable[[_C], _C]: ...

def fields(cls: type) -> Tuple[Attribute, ...]: ...
def validate(inst: Any) -> None: ...

# we use Any instead of _CountingAttr so that e.g. `make_class('Foo', [attr.ib()])` is valid
def make_class(name, attrs: Union[List[str], Dict[str, Any]], bases: Tuple[type, ...] = ..., **attributes_arguments) -> type: ...

# _funcs --

# FIXME: asdict/astuple do not honor their factory args.  waiting on one of these:
# https://github.com/python/mypy/issues/4236
# https://github.com/python/typing/issues/253
def asdict(inst: Any, recurse: bool = ..., filter: Optional[_FilterType] = ..., dict_factory: Type[Mapping] = ..., retain_collection_types: bool = ...) -> Dict[str, Any]: ...
def astuple(inst: Any, recurse: bool = ..., filter: Optional[_FilterType] = ..., tuple_factory: Type[Sequence] = ..., retain_collection_types: bool = ...) -> Tuple[Any, ...]: ...

def has(cls: type) -> bool: ...
def assoc(inst: _T, **changes: Any) -> _T: ...
def evolve(inst: _T, **changes: Any) -> _T: ...

# _config --

def set_run_validators(run: bool) -> None: ...
def get_run_validators() -> bool: ...

# aliases
s = attributes = attrs
ib = attr = attrib
dataclass = attrs # Technically, partial(attrs, auto_attribs=True) ;)
