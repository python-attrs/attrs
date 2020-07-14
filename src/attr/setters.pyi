from . import _OnSetAttrType, Attribute
from typing import TypeVar, Any, NewType, NoReturn, cast

_T = TypeVar("_T")

def frozen(
    instance: Any, attribute: Attribute, new_value: Any
) -> NoReturn: ...
def pipe(*setters: _OnSetAttrType) -> _OnSetAttrType: ...
def validate(instance: Any, attribute: Attribute, new_value: _T) -> _T: ...
def convert(instance: Any, attribute: Attribute, new_value: _T) -> _T: ...

_DisableType = NewType("_DisableType", object)
DISABLE: _DisableType
