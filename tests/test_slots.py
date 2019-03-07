"""
Unit tests for slot-related functionality.
"""
import pickle
import weakref

import pytest

import attr

from attr._compat import PY2, PYPY, just_warn, make_set_closure_cell


# Pympler doesn't work on PyPy.
try:
    from pympler.asizeof import asizeof

    has_pympler = True
except BaseException:  # Won't be an import error.
    has_pympler = False


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

    if not PY2:

        def my_class(self):
            return __class__  # NOQA: F821

        def my_super(self):
            """Just to test out the no-arg super."""
            return super().__repr__()


@attr.s(slots=True, hash=True)
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

    if not PY2:

        def my_class(self):
            return __class__  # NOQA: F821

        def my_super(self):
            """Just to test out the no-arg super."""
            return super().__repr__()


def test_slots_being_used():
    """
    The class is really using __slots__.
    """
    non_slot_instance = C1(x=1, y="test")
    slot_instance = C1Slots(x=1, y="test")

    assert "__dict__" not in dir(slot_instance)
    assert "__slots__" in dir(slot_instance)

    assert "__dict__" in dir(non_slot_instance)
    assert "__slots__" not in dir(non_slot_instance)

    assert set(["__weakref__", "x", "y"]) == set(slot_instance.__slots__)

    if has_pympler:
        assert asizeof(slot_instance) < asizeof(non_slot_instance)

    non_slot_instance.t = "test"
    with pytest.raises(AttributeError):
        slot_instance.t = "test"

    assert 1 == non_slot_instance.method()
    assert 1 == slot_instance.method()

    assert attr.fields(C1Slots) == attr.fields(C1)
    assert attr.asdict(slot_instance) == attr.asdict(non_slot_instance)


def test_basic_attr_funcs():
    """
    Comparison, `__eq__`, `__hash__`, `__repr__`, `attrs.asdict` work.
    """
    a = C1Slots(x=1, y=2)
    b = C1Slots(x=1, y=3)
    a_ = C1Slots(x=1, y=2)

    # Comparison.
    assert b > a

    assert a_ == a

    # Hashing.
    hash(b)  # Just to assert it doesn't raise.

    # Repr.
    assert "C1Slots(x=1, y=2)" == repr(a)

    assert {"x": 1, "y": 2} == attr.asdict(a)


def test_inheritance_from_nonslots():
    """
    Inheritance from a non-slot class works.

    Note that a slotted class inheriting from an ordinary class loses most of
    the benefits of slotted classes, but it should still work.
    """

    @attr.s(slots=True, hash=True)
    class C2Slots(C1):
        z = attr.ib()

    c2 = C2Slots(x=1, y=2, z="test")

    assert 1 == c2.x
    assert 2 == c2.y
    assert "test" == c2.z

    c2.t = "test"  # This will work, using the base class.

    assert "test" == c2.t

    assert 1 == c2.method()
    assert "clsmethod" == c2.classmethod()
    assert "staticmethod" == c2.staticmethod()

    assert set(["z"]) == set(C2Slots.__slots__)

    c3 = C2Slots(x=1, y=3, z="test")

    assert c3 > c2

    c2_ = C2Slots(x=1, y=2, z="test")

    assert c2 == c2_

    assert "C2Slots(x=1, y=2, z='test')" == repr(c2)

    hash(c2)  # Just to assert it doesn't raise.

    assert {"x": 1, "y": 2, "z": "test"} == attr.asdict(c2)


def test_nonslots_these():
    """
    Enhancing a dict class using 'these' works.

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

    C2Slots = attr.s(
        these={"x": attr.ib(), "y": attr.ib(), "z": attr.ib()},
        init=False,
        slots=True,
        hash=True,
    )(SimpleOrdinaryClass)

    c2 = C2Slots(x=1, y=2, z="test")
    assert 1 == c2.x
    assert 2 == c2.y
    assert "test" == c2.z
    with pytest.raises(AttributeError):
        c2.t = "test"  # We have slots now.

    assert 1 == c2.method()
    assert "clsmethod" == c2.classmethod()
    assert "staticmethod" == c2.staticmethod()

    assert set(["__weakref__", "x", "y", "z"]) == set(C2Slots.__slots__)

    c3 = C2Slots(x=1, y=3, z="test")
    assert c3 > c2
    c2_ = C2Slots(x=1, y=2, z="test")
    assert c2 == c2_

    assert "SimpleOrdinaryClass(x=1, y=2, z='test')" == repr(c2)

    hash(c2)  # Just to assert it doesn't raise.

    assert {"x": 1, "y": 2, "z": "test"} == attr.asdict(c2)


def test_inheritance_from_slots():
    """
    Inheriting from an attr slot class works.
    """

    @attr.s(slots=True, hash=True)
    class C2Slots(C1Slots):
        z = attr.ib()

    @attr.s(slots=True, hash=True)
    class C2(C1):
        z = attr.ib()

    c2 = C2Slots(x=1, y=2, z="test")
    assert 1 == c2.x
    assert 2 == c2.y
    assert "test" == c2.z

    assert set(["z"]) == set(C2Slots.__slots__)

    assert 1 == c2.method()
    assert "clsmethod" == c2.classmethod()
    assert "staticmethod" == c2.staticmethod()

    with pytest.raises(AttributeError):
        c2.t = "test"

    non_slot_instance = C2(x=1, y=2, z="test")
    if has_pympler:
        assert asizeof(c2) < asizeof(non_slot_instance)

    c3 = C2Slots(x=1, y=3, z="test")
    assert c3 > c2
    c2_ = C2Slots(x=1, y=2, z="test")
    assert c2 == c2_

    assert "C2Slots(x=1, y=2, z='test')" == repr(c2)

    hash(c2)  # Just to assert it doesn't raise.

    assert {"x": 1, "y": 2, "z": "test"} == attr.asdict(c2)


def test_bare_inheritance_from_slots():
    """
    Inheriting from a bare attr slot class works.
    """

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

    @attr.s(slots=True, hash=True)
    class C2Slots(C1BareSlots):
        z = attr.ib()

    @attr.s(slots=True, hash=True)
    class C2(C1Bare):
        z = attr.ib()

    c2 = C2Slots(x=1, y=2, z="test")
    assert 1 == c2.x
    assert 2 == c2.y
    assert "test" == c2.z

    assert 1 == c2.method()
    assert "clsmethod" == c2.classmethod()
    assert "staticmethod" == c2.staticmethod()

    with pytest.raises(AttributeError):
        c2.t = "test"

    non_slot_instance = C2(x=1, y=2, z="test")
    if has_pympler:
        assert asizeof(c2) < asizeof(non_slot_instance)

    c3 = C2Slots(x=1, y=3, z="test")
    assert c3 > c2
    c2_ = C2Slots(x=1, y=2, z="test")
    assert c2 == c2_

    assert "C2Slots(x=1, y=2, z='test')" == repr(c2)

    hash(c2)  # Just to assert it doesn't raise.

    assert {"x": 1, "y": 2, "z": "test"} == attr.asdict(c2)


@pytest.mark.skipif(PY2, reason="closure cell rewriting is PY3-only.")
class TestClosureCellRewriting(object):
    def test_closure_cell_rewriting(self):
        """
        Slot classes support proper closure cell rewriting.

        This affects features like `__class__` and the no-arg super().
        """
        non_slot_instance = C1(x=1, y="test")
        slot_instance = C1Slots(x=1, y="test")

        assert non_slot_instance.my_class() is C1
        assert slot_instance.my_class() is C1Slots

        # Just assert they return something, and not an exception.
        assert non_slot_instance.my_super()
        assert slot_instance.my_super()

    def test_inheritance(self):
        """
        Slot classes support proper closure cell rewriting when inheriting.

        This affects features like `__class__` and the no-arg super().
        """

        @attr.s
        class C2(C1):
            def my_subclass(self):
                return __class__  # NOQA: F821

        @attr.s
        class C2Slots(C1Slots):
            def my_subclass(self):
                return __class__  # NOQA: F821

        non_slot_instance = C2(x=1, y="test")
        slot_instance = C2Slots(x=1, y="test")

        assert non_slot_instance.my_class() is C1
        assert slot_instance.my_class() is C1Slots

        # Just assert they return something, and not an exception.
        assert non_slot_instance.my_super()
        assert slot_instance.my_super()

        assert non_slot_instance.my_subclass() is C2
        assert slot_instance.my_subclass() is C2Slots

    @pytest.mark.parametrize("slots", [True, False])
    def test_cls_static(self, slots):
        """
        Slot classes support proper closure cell rewriting for class- and
        static methods.
        """
        # Python can reuse closure cells, so we create new classes just for
        # this test.

        @attr.s(slots=slots)
        class C:
            @classmethod
            def clsmethod(cls):
                return __class__  # noqa: F821

        assert C.clsmethod() is C

        @attr.s(slots=slots)
        class D:
            @staticmethod
            def statmethod():
                return __class__  # noqa: F821

        assert D.statmethod() is D

    @pytest.mark.skipif(PYPY, reason="ctypes are used only on CPython")
    def test_missing_ctypes(self, monkeypatch):
        """
        Keeps working if ctypes is missing.

        A warning is emitted that points to the actual code.
        """
        monkeypatch.setattr(attr._compat, "import_ctypes", lambda: None)
        func = make_set_closure_cell()

        with pytest.warns(RuntimeWarning) as wr:
            func()

        w = wr.pop()
        assert __file__ == w.filename
        assert (
            "Missing ctypes.  Some features like bare super() or accessing "
            "__class__ will not work with slotted classes.",
        ) == w.message.args

        assert just_warn is func


@pytest.mark.skipif(PYPY, reason="__slots__ only block weakref on CPython")
def test_not_weakrefable():
    """
    Instance is not weak-referenceable when `weakref_slot=False` in CPython.
    """

    @attr.s(slots=True, weakref_slot=False)
    class C(object):
        pass

    c = C()

    with pytest.raises(TypeError):
        weakref.ref(c)


@pytest.mark.skipif(
    not PYPY, reason="slots without weakref_slot should only work on PyPy"
)
def test_implicitly_weakrefable():
    """
    Instance is weak-referenceable even when `weakref_slot=False` in PyPy.
    """

    @attr.s(slots=True, weakref_slot=False)
    class C(object):
        pass

    c = C()
    w = weakref.ref(c)

    assert c is w()


def test_weakrefable():
    """
    Instance is weak-referenceable when `weakref_slot=True`.
    """

    @attr.s(slots=True, weakref_slot=True)
    class C(object):
        pass

    c = C()
    w = weakref.ref(c)

    assert c is w()


def test_weakref_does_not_add_a_field():
    """
    `weakref_slot=True` does not add a field to the class.
    """

    @attr.s(slots=True, weakref_slot=True)
    class C(object):
        field = attr.ib()

    assert [f.name for f in attr.fields(C)] == ["field"]


def tests_weakref_does_not_add_when_inheriting_with_weakref():
    """
    `weakref_slot=True` does not add a new __weakref__ slot when inheriting
    one.
    """

    @attr.s(slots=True, weakref_slot=True)
    class C(object):
        pass

    @attr.s(slots=True, weakref_slot=True)
    class D(C):
        pass

    d = D()
    w = weakref.ref(d)

    assert d is w()


def tests_weakref_does_not_add_with_weakref_attribute():
    """
    `weakref_slot=True` does not add a new __weakref__ slot when an attribute
    of that name exists.
    """

    @attr.s(slots=True, weakref_slot=True)
    class C(object):
        __weakref__ = attr.ib(init=False, hash=False, repr=False, cmp=False)

    c = C()
    w = weakref.ref(c)

    assert c is w()


def _loads_dumps(instance):
    """
    Pickle loads-dumps round trip test helper.
    """
    return pickle.loads(pickle.dumps(instance))


def test_getstate_setstate_auto_generated():
    """
    __getstate__ and __setstate__ are auto generated (if not implemented).
    """
    c1 = C1Slots(x=10, y=2)
    assert (10, 2) == c1.__getstate__()

    c1.__setstate__((1, 0))
    assert C1Slots(x=1, y=0) == c1

    c1_new = _loads_dumps(C1Slots(x=11, y=22))
    assert C1Slots(x=11, y=22) == c1_new


@attr.s(slots=True, hash=True)
class SubC1Slots(C1Slots):
    z = attr.ib()


@attr.s(slots=True, hash=True)
class SubC1(C1):
    z = attr.ib()


def test_subclass_getstate_setstate_auto_generated():
    """
    Autogenerated __getstate__ and __setstate__  works for subclasses.
    """
    for subclass in [SubC1, SubC1Slots]:
        sc1 = subclass(x=1, y=2, z="z")
        assert (1, 2, "z") == sc1.__getstate__()

        sc1.__setstate__((10, 0, "zz"))
        assert subclass(x=10, y=0, z="zz") == sc1

        sc1_new = _loads_dumps(subclass(x=11, y=22, z="zz"))
        assert subclass(x=11, y=22, z="zz") == sc1_new


@attr.s(slots=True)
class CustomGetSetState(object):
    a = attr.ib()
    b = attr.ib()

    def __getstate__(self):
        """Modify value for `b` just to test that this method is called."""
        return self.a, self.b + "_placeholder"

    def __setstate__(self, state):
        """Modify value for `b` just to test that this method is called."""
        self.a, self.b = state
        self.b += "_reconstructed"


@attr.s(slots=True)
class SubCustomGetSetState(CustomGetSetState):
    c = attr.ib()

    def __getstate__(self):
        return super(SubCustomGetSetState, self).__getstate__() + tuple(self.c)

    def __setstate__(self, state):
        super(SubCustomGetSetState, self).__setstate__(state[:2])
        self.c = state[-1]


@attr.s(slots=True)
class SubCustomGetSetStateNoOverride(CustomGetSetState):
    c = attr.ib()


def test_custom_getstate_setstate_effective():
    """
    Custom __getstate__ and __setstate__ are used when implemented.
    """
    c = CustomGetSetState("a", "b")
    assert ("a", "b_placeholder") == c.__getstate__()

    c.__setstate__(("other_a", "b"))
    assert CustomGetSetState("other_a", "b_reconstructed") == c

    c_new = _loads_dumps(CustomGetSetState("a", "b"))
    assert CustomGetSetState("a", "b_placeholder_reconstructed") == c_new


def test_subclass_custom_getstate_setstate_referencing_super():
    """
    Custom __getstate__ and __setstate__ referencing super class ok.
    """
    sc = SubCustomGetSetState("a", "b", "c")
    assert ("a", "b_placeholder", "c") == sc.__getstate__()

    sc.__setstate__(("a", "b", "other_c"))
    assert SubCustomGetSetState("a", "b_reconstructed", "other_c") == sc

    sc_new = _loads_dumps(SubCustomGetSetState("a", "b", "c"))
    assert (
        SubCustomGetSetState("a", "b_placeholder_reconstructed", "c") == sc_new
    )


def test_subclass_custom_getstate_setstate_no_override():
    """
    No overriding of custom __getstate__ and __setstate__ -> superclass
    implementation.
    """
    sc = SubCustomGetSetStateNoOverride("a", "b", "c")
    assert ("a", "b_placeholder") == sc.__getstate__()

    sc.__setstate__(("a", "bb"))
    assert SubCustomGetSetStateNoOverride("a", "bb_reconstructed", "c") == sc

    sc_new = _loads_dumps(SubCustomGetSetStateNoOverride("a", "b", "c"))
    with pytest.raises(AttributeError):
        sc_new.c

    assert "a" == sc_new.a
    assert "b_placeholder_reconstructed" == sc_new.b


def test_raise_if_getstate_and_not_setstate_implemented():
    """
    ValueError raised if only one of __getstate__, __setstate__ implemented.
    """
    with pytest.raises(ValueError):

        @attr.s(slots=True)
        class CustomGetStateOnly(object):
            a = attr.ib()

            def __getstate__(self):
                return self.a
