"""Unit tests for slot-related functionality."""
import pytest

# Pympler doesn't work on PyPy.
try:
    from pympler.asizeof import asizeof
    has_pympler = True
except:  # Won't be an import error.
    has_pympler = False

import attr


@attr.s
class C1(object):
    x = attr.ib(validator=attr.validators.instance_of(int))
    y = attr.ib()

    def method(self):
        return self.x

    @classmethod
    def classmethod(cls):
        return "clsmethod"

    @staticmethod
    def staticmethod():
        return "staticmethod"


@attr.s(slots=True)
class C1Slots(object):
    x = attr.ib(validator=attr.validators.instance_of(int))
    y = attr.ib()

    def method(self):
        return self.x

    @classmethod
    def classmethod(cls):
        return "clsmethod"

    @staticmethod
    def staticmethod():
        return "staticmethod"


def test_slots_being_used():
    """Test whether the class really is using __slots__."""
    non_slot_instance = C1(x=1, y="test")
    slot_instance = C1Slots(x=1, y="test")

    assert "__dict__" not in dir(slot_instance)
    assert "__slots__" in dir(slot_instance)

    assert "__dict__" in dir(non_slot_instance)
    assert "__slots__" not in dir(non_slot_instance)

    assert set(slot_instance.__slots__) == set(["x", "y"])

    if has_pympler:
        assert asizeof(slot_instance) < asizeof(non_slot_instance)

    non_slot_instance.t = "test"
    with pytest.raises(AttributeError):
        slot_instance.t = "test"

    assert non_slot_instance.method() == 1
    assert slot_instance.method() == 1

    assert attr.fields(C1Slots) == attr.fields(C1)
    assert attr.asdict(slot_instance) == attr.asdict(non_slot_instance)


def test_basic_attr_funcs():
    """Test basic attr functionality on a simple slots class."""
    a = C1Slots(x=1, y=2)
    b = C1Slots(x=1, y=3)
    a_ = C1Slots(x=1, y=2)

    # Comparison.
    assert b > a

    assert a_ == a

    # Hashing.
    hash(b)  # Just to assert it doesn't raise.

    # Repr.
    assert repr(a) == "C1Slots(x=1, y=2)"

    assert attr.asdict(a) == {"x": 1, "y": 2}


def test_inheritance_from_nonslots():
    """Test whether inheriting from an attr class works.

    Note that a slots class inheriting from an ordinary class loses most of the
    benefits of slots classes, but it should still work.
    """
    @attr.s(slots=True)
    class C2Slots(C1):
        z = attr.ib()

    c2 = C2Slots(x=1, y=2, z="test")
    assert c2.x == 1
    assert c2.y == 2
    assert c2.z == "test"
    c2.t = "test"  # This will work, using the base class.
    assert c2.t == "test"

    assert c2.method() == 1
    assert c2.classmethod() == "clsmethod"
    assert c2.staticmethod() == "staticmethod"

    assert set(C2Slots.__slots__) == set(["z"])

    c3 = C2Slots(x=1, y=3, z="test")
    assert c3 > c2
    c2_ = C2Slots(x=1, y=2, z="test")
    assert c2 == c2_

    assert repr(c2) == "C2Slots(x=1, y=2, z='test')"

    hash(c2)  # Just to assert it doesn't raise.

    assert attr.asdict(c2) == {"x": 1, "y": 2, "z": "test"}


def test_nonslots_these():
    """Test enhancing a non-slots class using 'these'.

    This will actually *replace* the class with another one, using slots.
    """
    class SimpleOrdinaryClass(object):
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

        def method(self):
            return self.x

        @classmethod
        def classmethod(cls):
            return "clsmethod"

        @staticmethod
        def staticmethod():
            return "staticmethod"

    C2Slots = attr.s(these={"x": attr.ib(), "y": attr.ib(), "z": attr.ib()},
                     init=False, slots=True)(SimpleOrdinaryClass)

    c2 = C2Slots(x=1, y=2, z="test")
    assert c2.x == 1
    assert c2.y == 2
    assert c2.z == "test"
    with pytest.raises(AttributeError):
        c2.t = "test"  # We have slots now.

    assert c2.method() == 1
    assert c2.classmethod() == "clsmethod"
    assert c2.staticmethod() == "staticmethod"

    assert set(C2Slots.__slots__) == set(["x", "y", "z"])

    c3 = C2Slots(x=1, y=3, z="test")
    assert c3 > c2
    c2_ = C2Slots(x=1, y=2, z="test")
    assert c2 == c2_

    assert repr(c2) == "SimpleOrdinaryClass(x=1, y=2, z='test')"

    hash(c2)  # Just to assert it doesn't raise.

    assert attr.asdict(c2) == {"x": 1, "y": 2, "z": "test"}


def test_inheritance_from_slots():
    """Test whether inheriting from an attr slot class works."""
    @attr.s(slots=True)
    class C2Slots(C1Slots):
        z = attr.ib()

    @attr.s(slots=True)
    class C2(C1):
        z = attr.ib()

    c2 = C2Slots(x=1, y=2, z="test")
    assert c2.x == 1
    assert c2.y == 2
    assert c2.z == "test"

    assert set(C2Slots.__slots__) == set(["z"])

    assert c2.method() == 1
    assert c2.classmethod() == "clsmethod"
    assert c2.staticmethod() == "staticmethod"

    with pytest.raises(AttributeError):
        c2.t = "test"

    non_slot_instance = C2(x=1, y=2, z="test")
    if has_pympler:
        assert asizeof(c2) < asizeof(non_slot_instance)

    c3 = C2Slots(x=1, y=3, z="test")
    assert c3 > c2
    c2_ = C2Slots(x=1, y=2, z="test")
    assert c2 == c2_

    assert repr(c2) == "C2Slots(x=1, y=2, z='test')"

    hash(c2)  # Just to assert it doesn't raise.

    assert attr.asdict(c2) == {"x": 1, "y": 2, "z": "test"}


def test_bare_inheritance_from_slots():
    """Test whether inheriting from a bare attr slot class works."""
    @attr.s(init=False, cmp=False, hash=False, repr=False, slots=True)
    class C1BareSlots(object):
        x = attr.ib(validator=attr.validators.instance_of(int))
        y = attr.ib()

        def method(self):
            return self.x

        @classmethod
        def classmethod(cls):
            return "clsmethod"

        @staticmethod
        def staticmethod():
            return "staticmethod"

    @attr.s(init=False, cmp=False, hash=False, repr=False)
    class C1Bare(object):
        x = attr.ib(validator=attr.validators.instance_of(int))
        y = attr.ib()

        def method(self):
            return self.x

        @classmethod
        def classmethod(cls):
            return "clsmethod"

        @staticmethod
        def staticmethod():
            return "staticmethod"

    @attr.s(slots=True)
    class C2Slots(C1BareSlots):
        z = attr.ib()

    @attr.s(slots=True)
    class C2(C1Bare):
        z = attr.ib()

    c2 = C2Slots(x=1, y=2, z="test")
    assert c2.x == 1
    assert c2.y == 2
    assert c2.z == "test"

    assert c2.method() == 1
    assert c2.classmethod() == "clsmethod"
    assert c2.staticmethod() == "staticmethod"

    with pytest.raises(AttributeError):
        c2.t = "test"

    non_slot_instance = C2(x=1, y=2, z="test")
    if has_pympler:
        assert asizeof(c2) < asizeof(non_slot_instance)

    c3 = C2Slots(x=1, y=3, z="test")
    assert c3 > c2
    c2_ = C2Slots(x=1, y=2, z="test")
    assert c2 == c2_

    assert repr(c2) == "C2Slots(x=1, y=2, z='test')"

    hash(c2)  # Just to assert it doesn't raise.

    assert attr.asdict(c2) == {"x": 1, "y": 2, "z": "test"}
