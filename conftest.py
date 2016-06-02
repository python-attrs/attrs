from __future__ import absolute_import, division, print_function

import os

import pytest
from hypothesis import settings


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

# PyPy on Travis appears to be too slow.
settings.register_profile("travis_pypy", settings(perform_health_check=False))
settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))
