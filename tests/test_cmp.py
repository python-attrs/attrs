"""
Tests for equality and ordering methods from `attrib._make`
when a CompSpec object is specified.
"""

import pytest

import attr

from .utils import simple_class


EqC = simple_class(eq=True)
EqCSlots = simple_class(eq=True, slots=True)


# ObjRequiringCustomEq is a simple object that throw an ValueError when
# we naively try obj1 == obj2. This simulates what happens when we compare
# numpy arrays or pandas dataframes.
@attr.s(eq=False)
class ObjRequiringCustomEq(object):

    value = attr.ib()

    def __eq__(self, other):
        raise ValueError("Can't compare ObjRequiringCustomEq using __eq__")


class TestCmpSpec(object):
    """
    Tests for equality and ordering when a CompSpec object is specified.
    """

    @pytest.mark.parametrize("cls", [EqC, EqCSlots])
    def test_eq_exception(self, cls):
        """
        Test for eq method when attribute does not conform to default protocol.
        """
        with pytest.raises(ValueError):
            cls(ObjRequiringCustomEq(1), 2) == cls(ObjRequiringCustomEq(1), 2)
        with pytest.raises(ValueError):
            cls(ObjRequiringCustomEq(1), 2) != cls(ObjRequiringCustomEq(1), 2)
