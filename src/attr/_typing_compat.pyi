from typing import Any, ClassVar, Protocol

MYPY = False

# A protocol to be able to statically accept an attrs class.
class AttrsInstance(Protocol):
    __attrs_attrs__: ClassVar[Any]

if MYPY:
    AttrsInstance_ = AttrsInstance
else:
    AttrsInstance_ = Any
