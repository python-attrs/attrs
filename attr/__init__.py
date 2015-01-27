# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ._funcs import (
    ls,
    to_dict,
)
from ._make import (
    _make_attr as ib,
    s,
)

__version__ = "0.0.0.dev0"
__author__ = "Hynek Schlawack"
__license__ = "MIT"
__copyright__ = "Copyright 2015 Hynek Schlawack"


__all__ = [
    "ib", "s", "ls", "to_dict",
]
