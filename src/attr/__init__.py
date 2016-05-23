from __future__ import absolute_import, division, print_function

from ._funcs import (
    asdict,
    assoc,
    has,
)
from ._make import (
    Attribute,
    Factory,
    NOTHING,
    attr,
    attributes,
    fields,
    make_class,
    validate,
)
from ._config import (
    get_run_validators,
    set_run_validators,
)
from . import filters
from . import validators


__version__ = "16.0.0"

__title__ = "attrs"
__description__ = "Attributes without boilerplate."
__uri__ = "https://attrs.readthedocs.io/"

__author__ = "Hynek Schlawack"
__email__ = "hs@ox.cx"

__license__ = "MIT"
__copyright__ = "Copyright (c) 2015 Hynek Schlawack"


s = attributes
attr = ib = attr

__all__ = [
    "Attribute",
    "Factory",
    "NOTHING",
    "asdict",
    "assoc",
    "attr",
    "attributes",
    "fields",
    "filters",
    "get_run_validators",
    "has",
    "ib",
    "make_class",
    "s",
    "set_run_validators",
    "validate",
    "validators",
]
