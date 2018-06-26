"""
Tests for `attr.converters`.
"""

from __future__ import absolute_import

import pytest

from attr import attrib
from attr.converters import optional


class TestOptional(object):
    """
    Tests for `optional`.
    """

    def test_success_with_type(self):
        """
        Wrapped converter is used as usual if value is not None.
        """
        c = optional(int)
        assert c("42") == 42

    def test_success_with_none(self):
        """
        Nothing happens if None.
        """
        c = optional(int)
        assert c(None) is None

    def test_fail(self):
        """
        Propagates the underlying conversion error when conversion fails.
        """
        c = optional(int)
        with pytest.raises(ValueError):
            c("not_an_int")


class TestOptionalWarningWarning(object):

    def test_warn_type_optional(self):
        with pytest.warns(Warning) as record:
            attrib(default=None, converter=int)
        msg = list(record)[0]
        assert "consider using " in str(msg)
