from __future__ import absolute_import, division, print_function

import sys


PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2


if PY2:
    # TYPE is used in exceptions, repr(int) is different on Python 2 and 3.
    TYPE = "type"

    def exec_(code, locals_, globals_):
        exec("exec code in locals_, globals_")

    def iteritems(d):
        return d.iteritems()
else:
    TYPE = "class"

    def exec_(code, locals_, globals_):
        exec(code, locals_, globals_)

    def iteritems(d):
        return d.items()
