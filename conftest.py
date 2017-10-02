from __future__ import absolute_import, division, print_function

import sys
import pytest


@pytest.fixture(scope="session")
def C():
    """
    Return a simple but fully featured attrs class with an x and a y attribute.
    """
    from attr import attrs, attrib

    @attrs
    class C(object):
        x = attrib()
        y = attrib()

    return C


collect_ignore = []
if sys.version_info[:2] < (3, 6):
    collect_ignore.append("tests/test_annotations.py")
