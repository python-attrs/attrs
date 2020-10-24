from __future__ import absolute_import

import pytest

import attr

from attr._compat import PY2, ReadOnlyDict


class TestReadOnlyDict(object):
    def test___delitem__(self):
        """
        One cannot delete from a read-only structure
        """

        with pytest.raises(TypeError, match="'mappingproxy' object does not support item deletion"):
            del ReadOnlyDict()['5']

    def test_pop(self):
        """
        One cannot pop from a read-only structure
        """

        with pytest.raises(AttributeError, match="'mappingproxy' object has no attribute 'pop'"):
            ReadOnlyDict().pop()

