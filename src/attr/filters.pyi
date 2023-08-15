from typing import Any

from . import Attribute, _FilterType


def include(*what: type | str | Attribute[Any]) -> _FilterType[Any]: ...
def exclude(*what: type | str | Attribute[Any]) -> _FilterType[Any]: ...
