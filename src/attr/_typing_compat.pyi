from typing import Any, ClassVar, Protocol

MYPY = False

if MYPY:
    # A protocol to be able to statically accept an attrs class.
    class AttrsInstance_(Protocol):
        __attrs_attrs__: ClassVar[Any]

else:
    class AttrsInstance_(Protocol):
        pass
