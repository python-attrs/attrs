# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ._funcs import (
    asdict,
    assoc,
    fields,
    has,
    valid,
)
from ._make import (
    Attribute,
    Factory,
    NOTHING,
    attr,
    attributes,
    make_class,
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
    "valid",
    "validators",
]
