# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ._funcs import (
    ls,
    to_dict,
    has,
)
from ._make import (
    Attribute,
    _add_methods as s,
    _make_attr as ib,
)

__version__ = "15.0.0.dev0"
__author__ = "Hynek Schlawack"
__license__ = "MIT"
__copyright__ = "Copyright 2015 Hynek Schlawack"


__all__ = [
    "Attribute", "has", "ib", "s", "ls", "to_dict",
]
