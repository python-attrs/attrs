"""
Python 3-only integration tests for provisional next generation APIs.
"""

import pytest

import attr


@attr.define
class C:
    x: str
    y: int


class TestNextGen:
    def test_simple(self):
        """
        Instantiation works.
        """
        C("1", 2)

    def test_no_slots(self):
        """
        slots can be deactivated.
        """

        @attr.define(slots=False)
        class NoSlots:
            x: int

        ns = NoSlots(1)

        assert {"x": 1} == getattr(ns, "__dict__")

    def test_validates(self):
        """
        Validators at __init__ and __setattr__ work.
        """

        @attr.define
        class Validated:
            x: int = attr.field(validator=attr.validators.instance_of(int))

        v = Validated(1)

        with pytest.raises(TypeError):
            Validated(None)

        with pytest.raises(TypeError):
            v.x = "1"

    def test_no_order(self):
        """
        Order is off by default but can be added.
        """
        with pytest.raises(TypeError):
            C("1", 2) < C("2", 3)

        @attr.define(order=True)
        class Ordered:
            x: int

        assert Ordered(1) < Ordered(2)

    def test_override_auto_attribs_true(self):
        """
        Don't guess if auto_attrib is set explicitly.

        Having an unannotated attr.ib/attr.field fails.
        """
        with pytest.raises(attr.exceptions.UnannotatedAttributeError):

            @attr.define(auto_attribs=True)
            class ThisFails:
                x = attr.field()
                y: int

    def test_override_auto_attribs_false(self):
        """
        Don't guess if auto_attrib is set explicitly.

        Annotated fields that don't carry an attr.ib are ignored.
        """

        @attr.define(auto_attribs=False)
        class NoFields:
            x: int
            y: int

        assert NoFields() == NoFields()

    def test_auto_attribs_detect(self):
        """
        define correctly detects if a class lacks type annotations.
        """

        @attr.define
        class OldSchool:
            x = attr.field()

        assert OldSchool(1) == OldSchool(1)

    def test_exception(self):
        """
        Exceptions are detected and correctly handled.
        """

        @attr.define
        class E(Exception):
            msg: str
            other: int

        with pytest.raises(E) as ei:
            raise E("yolo", 42)

        e = ei.value

        assert ("yolo", 42) == e.args
        assert "yolo" == e.msg
        assert 42 == e.other

    def test_frozen(self):
        """
        attr.frozen freezes classes.
        """

        @attr.frozen
        class F:
            x: str

        f = F(1)

        with pytest.raises(attr.exceptions.FrozenInstanceError):
            f.x = 2
