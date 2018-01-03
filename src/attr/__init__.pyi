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
    validator: Optional[_ValidatorType[_T]]
    repr: bool
    cmp: bool
    hash: Optional[bool]
    init: bool
    converter: Optional[_ConverterType[_T]]
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

# FIXME: We had several choices for the annotation to use for type arg:
# 1) Type[_T]
#   - Pros: works in PyCharm without plugin support
#   - Cons: produces less informative error in the case of conflicting TypeVars
#     e.g. `attr.ib(default='bad', type=int)`
# 2) Callable[..., _T]
#   - Pros: more informative errors than #1
#   - Cons: validator tests results in confusing error.
#     e.g. `attr.ib(type=int, validator=validate_str)`
# 3) type
#   - Pros: in mypy, the behavior of type argument is exactly the same as with
#     annotations.
#   - Cons: completely disables type inspections in PyCharm when using the
#     type arg.
# We chose option #1 until either PyCharm adds support for attrs, or python 2
# reaches EOL.

# NOTE: If you update these update `ib` and `attr` below.
# 1st form catches _T set.
@overload
def attrib(default: Optional[_T] = ..., validator: Optional[_ValidatorArgType[_T]] = ...,
           repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ...,
           metadata: Mapping = ..., type: Optional[Type[_T]] = ...,
           converter: Optional[_ConverterType[_T]] = ...) -> _T: ...
# 2nd form no _T , so returns Any.
@overload
def attrib(default: None = ..., validator: None = ...,
           repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ...,
           metadata: Mapping = ..., type: None = ...,
           converter: None = ...) -> Any: ...

# Note: If you update these update `s` and `attributes` below.
@overload
def attrs(
    maybe_cls: _C, these: Optional[Dict[str, Any]] = ...,
    repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ...,
    hash: Optional[bool] = ..., init: bool = ..., slots: bool = ...,
    frozen: bool = ..., str: bool = ...) -> _C: ...
@overload
def attrs(
    maybe_cls: None = ..., these: Optional[Dict[str, Any]] = ...,
    repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ...,
    hash: Optional[bool] = ..., init: bool = ..., slots: bool = ...,
    frozen: bool = ..., str: bool = ...) -> Callable[[_C], _C]: ...


# TODO: add support for returning NamedTuple from the mypy plugin
class _Fields(Tuple[Attribute, ...]):
    def __getattr__(self, name: str) -> Attribute: ...

def fields(cls: type) -> _Fields: ...
def validate(inst: Any) -> None: ...

# TODO: add support for returning a proper attrs class from the mypy plugin
# we use Any instead of _CountingAttr so that e.g. `make_class('Foo', [attr.ib()])` is valid
def make_class(name, attrs: Union[List[str], Dict[str, Any]],
               bases: Tuple[type, ...] = ...,
               **attributes_arguments) -> type: ...

# _funcs --

# TODO: add support for returning TypedDict from the mypy plugin
# FIXME: asdict/astuple do not honor their factory args.  waiting on one of these:
# https://github.com/python/mypy/issues/4236
# https://github.com/python/typing/issues/253
def asdict(inst: Any, recurse: bool = ..., filter: Optional[_FilterType] = ...,
           dict_factory: Type[Mapping] = ...,
           retain_collection_types: bool = ...) -> Dict[str, Any]: ...
# TODO: add support for returning NamedTuple from the mypy plugin
def astuple(inst: Any, recurse: bool = ..., filter: Optional[_FilterType] = ...,
            tuple_factory: Type[Sequence] = ...,
            retain_collection_types: bool = ...) -> Tuple[Any, ...]: ...

def has(cls: type) -> bool: ...
def assoc(inst: _T, **changes: Any) -> _T: ...
def evolve(inst: _T, **changes: Any) -> _T: ...

# _config --

def set_run_validators(run: bool) -> None: ...
def get_run_validators() -> bool: ...

# aliases --
#s = attributes = attrs
#ib = attr = attrib
#dataclass = attrs # Technically, partial(attrs, auto_attribs=True) ;)

# FIXME: there is a bug in PyCharm with creating aliases to overloads.
# Remove these when the bug is fixed:
# https://youtrack.jetbrains.com/issue/PY-27788

@overload
def ib(default: Optional[_T] = ..., validator: Optional[_ValidatorArgType[_T]] = ...,
           repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ...,
           metadata: Mapping = ..., type: Optional[Type[_T]] = ...,
           converter: Optional[_ConverterType[_T]] = ...) -> _T: ...
# 2nd form catches no type-setters. So returns Any.
@overload
def ib(default: None = ..., validator: None = ...,
           repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ...,
           metadata: Mapping = ..., type: None = ...,
           converter: None = ..., ) -> Any: ...
@overload
def attr(default: Optional[_T] = ..., validator: Optional[_ValidatorArgType[_T]] = ...,
           repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ...,
           metadata: Mapping = ..., type: Optional[Type[_T]] = ...,
           converter: Optional[_ConverterType[_T]] = ...) -> _T: ...
# 2nd form catches no type-setters. So returns Any.
@overload
def attr(default: None = ..., validator: None = ...,
           repr: bool = ..., cmp: bool = ..., hash: Optional[bool] = ..., init: bool = ...,
           metadata: Mapping = ..., type: None = ...,
           converter: None = ...) -> Any: ...


@overload
def attributes(
    maybe_cls: _C, these: Optional[Dict[str, Any]] = ...,
    repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ...,
    hash: Optional[bool] = ..., init: bool = ..., slots: bool = ...,
    frozen: bool = ..., str: bool = ...) -> _C: ...
@overload
def attributes(
    maybe_cls: None = ..., these: Optional[Dict[str, Any]] = ...,
    repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ...,
    hash: Optional[bool] = ..., init: bool = ..., slots: bool = ...,
    frozen: bool = ..., str: bool = ...) -> Callable[[_C], _C]: ...

@overload
def s(
    maybe_cls: _C, these: Optional[Dict[str, Any]] = ...,
    repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ...,
    hash: Optional[bool] = ..., init: bool = ..., slots: bool = ...,
    frozen: bool = ..., str: bool = ...) -> _C: ...
@overload
def s(
    maybe_cls: None = ..., these: Optional[Dict[str, Any]] = ...,
    repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ...,
    hash: Optional[bool] = ..., init: bool = ..., slots: bool = ...,
    frozen: bool = ..., str: bool = ...) -> Callable[[_C], _C]: ...

@overload
def dataclass(
    maybe_cls: _C, these: Optional[Dict[str, Any]] = ...,
    repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ...,
    hash: Optional[bool] = ..., init: bool = ..., slots: bool = ...,
    frozen: bool = ..., str: bool = ...) -> _C: ...
@overload
def dataclass(
    maybe_cls: None = ..., these: Optional[Dict[str, Any]] = ...,
    repr_ns: Optional[str] = ..., repr: bool = ..., cmp: bool = ...,
    hash: Optional[bool] = ..., init: bool = ..., slots: bool = ...,
    frozen: bool = ..., str: bool = ...) -> Callable[[_C], _C]: ...
# --