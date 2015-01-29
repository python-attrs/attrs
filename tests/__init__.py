# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


import sys


PY3 = sys.version_info[0] == 3
# TYPE is used in exceptions, repr(int) is differnt on Python 2 and 3.
TYPE = "class" if PY3 else "type"


def simple_attr(name):
    """
    Return an attribute with a name and no other bells and whistles.
    """
    from attr import Attribute
    from attr._dunders import NOTHING
    return Attribute(name=name, default_value=NOTHING, default_factory=NOTHING,
                     validator=None)
