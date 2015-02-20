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
from . import validators

__version__ = "15.0.0.dev1"
__author__ = "Hynek Schlawack"
__license__ = "MIT"
__copyright__ = "Copyright 2015 Hynek Schlawack"


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
    "has",
    "ib",
    "make_class",
    "s",
    "validate",
    "validators",
]
