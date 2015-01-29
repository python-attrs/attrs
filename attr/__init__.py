# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ._dunders import (
    NOTHING,
)
from ._funcs import (
    asdict,
    assoc,
    fields,
    has,
)
from ._make import (
    Attribute,
    attr,
    attributes,
)
from . import validators

__version__ = "15.0.0.dev0"
__author__ = "Hynek Schlawack"
__license__ = "MIT"
__copyright__ = "Copyright 2015 Hynek Schlawack"


s = attributes
attr = ib = attr

__all__ = [
    "Attribute",
    "NOTHING",
    "asdict",
    "assoc",
    "attr",
    "attributes",
    "fields",
    "has",
    "ib",
    "s",
    "validators",
]
