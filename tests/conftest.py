from __future__ import absolute_import, division, print_function


import pytest


@pytest.fixture(scope="session")
def C():
    """
    Return a simple but fully features attrs class with an x and a y attribute.
    """
    from attr import attributes, attr

    @attributes
    class C(object):
        x = attr()
        y = attr()

    return C
