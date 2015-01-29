# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


def simple_attr(name):
    """
    Return an attribute with a name and no other bells and whistles.
    """
    from attr import Attribute
    from attr._make import NOTHING
    return Attribute(name=name, default=NOTHING, validator=None)
