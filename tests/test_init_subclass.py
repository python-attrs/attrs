"""
Tests for `__init_subclass__` related tests.

Python 3.6+ only.
"""

import pytest

import attr


@pytest.mark.parametrize("slots", [True, False])
def test_init_subclass_vanilla(slots):
    """
    `super().__init_subclass__` can be used if the subclass is not an attrs
    class. This is problematic due to certain cell intricacies around static
    and class methods.
    """
    @attr.s(slots=slots)
    class Base:
        def __init_subclass__(cls, param, **kw):
            super().__init_subclass__(**kw)
            cls.param = param

    class Vanilla(Base, param="foo"):
        pass

    assert "foo" == Vanilla().param
