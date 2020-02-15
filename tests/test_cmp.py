"""
Tests for equality and ordering methods from `attrib._make`
when a CompSpec object is specified.
"""

import pytest

import attr

from .utils import simple_class


EqC = simple_class(eq=True)
EqCSlots = simple_class(eq=True, slots=True)
OrderC = simple_class(order=True)
OrderCSlots = simple_class(order=True, slots=True)


# ObjWithoutTruthValue is a simple object that has no truth value,
# e.g. __eq__ returns something other than a boolean, and Python
# tries to convert that non-boolean to a boolean by calling __bool__
# (or __nonzero__ in Python 2) on it.
#
# We could simulate this behaviour by simply throwing an exception from __eq__,
# but this complicated chain of events is more realistic because
# it mimics what happens when we compare numpy arrays and pandas dataframes.
@attr.s(eq=False)
class ObjWithoutTruthValue(object):

    value = attr.ib()

    def __eq__(self, other):
        return ObjWithoutTruthValue(self.value == other.value)

    def __lt__(self, other):
        return ObjWithoutTruthValue(self.value < other.value)

    def __bool__(self):
        raise ValueError("ObjWithoutTruthValue has no truth value.")

    __nonzero__ = __bool__  # Python 2

    @classmethod
    def compare(cls, obj, other):
        return (obj == other).value

    @classmethod
    def less_than(cls, obj, other):
        return (obj < other).value


class TestCmpSpec(object):
    """
    Tests for equality and ordering when a CompSpec object is specified.
    """

    @pytest.mark.parametrize("cls", [EqC, EqCSlots])
    def test_equality_exception(self, cls):
        """
        Test for equality methods when attribute has not truth value.
        """
        with pytest.raises(ValueError):
            cls(ObjWithoutTruthValue(1), 2) == cls(ObjWithoutTruthValue(1), 2)
        with pytest.raises(ValueError):
            cls(ObjWithoutTruthValue(1), 2) != cls(ObjWithoutTruthValue(1), 2)

    @pytest.mark.parametrize("cls", [OrderC, OrderCSlots])
    def test_order_exception(self, cls):
        """
        Test for ordering methods when attribute has not truth value.
        """
        with pytest.raises(ValueError):
            cls(ObjWithoutTruthValue(1), 2) < cls(ObjWithoutTruthValue(2), 2)
        with pytest.raises(ValueError):
            cls(ObjWithoutTruthValue(1), 2) > cls(ObjWithoutTruthValue(2), 2)
        with pytest.raises(ValueError):
            cls(ObjWithoutTruthValue(1), 2) <= cls(ObjWithoutTruthValue(2), 2)
        with pytest.raises(ValueError):
            cls(ObjWithoutTruthValue(1), 2) >= cls(ObjWithoutTruthValue(2), 2)
