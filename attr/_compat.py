# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import sys


PY3 = sys.version_info[0] == 3
# TYPE is used in exceptions, repr(int) is differnt on Python 2 and 3.
TYPE = "class" if PY3 else "type"

# I'm sorry. :(
if sys.version_info[0] == 2:
    def exec_(code, locals_, globals_):
        exec("exec code in locals_, globals_")
else:
    def exec_(code, locals_, globals_):
        exec(code, locals_, globals_)
