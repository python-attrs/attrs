"""
Python 3-only integration tests for provisional next generation APIs.
"""

import re

from functools import partial

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

        # Test with maybe_cls = None
        @attr.define()
        class OldSchool2:
            x = attr.field()

        assert OldSchool2(1) == OldSchool2(1)

    def test_auto_attribs_detect_annotations(self):
        """
        define correctly detects if a class has type annotations.
        """

        @attr.define
        class NewSchool:
            x: int

        assert NewSchool(1) == NewSchool(1)

        # Test with maybe_cls = None
        @attr.define()
        class NewSchool2:
            x: int

        assert NewSchool2(1) == NewSchool2(1)

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

    def test_auto_detect_eq(self):
        """
        auto_detect=True works for eq.

        Regression test for #670.
        """

        @attr.define
        class C:
            def __eq__(self, o):
                raise ValueError()

        with pytest.raises(ValueError):
            C() == C()

    def test_subclass_frozen(self):
        """
        It's possible to subclass an `attr.frozen` class and the frozen-ness is
        inherited.
        """

        @attr.frozen
        class A:
            a: int

        @attr.frozen
        class B(A):
            b: int

        @attr.define(on_setattr=attr.setters.NO_OP)
        class C(B):
            c: int

        assert B(1, 2) == B(1, 2)
        assert C(1, 2, 3) == C(1, 2, 3)

        with pytest.raises(attr.exceptions.FrozenInstanceError):
            A(1).a = 1

        with pytest.raises(attr.exceptions.FrozenInstanceError):
            B(1, 2).a = 1

        with pytest.raises(attr.exceptions.FrozenInstanceError):
            B(1, 2).b = 2

        with pytest.raises(attr.exceptions.FrozenInstanceError):
            C(1, 2, 3).c = 3

    def test_catches_frozen_on_setattr(self):
        """
        Passing frozen=True and on_setattr hooks is caught, even if the
        immutability is inherited.
        """

        @attr.define(frozen=True)
        class A:
            pass

        with pytest.raises(
            ValueError, match="Frozen classes can't use on_setattr."
        ):

            @attr.define(frozen=True, on_setattr=attr.setters.validate)
            class B:
                pass

        with pytest.raises(
            ValueError,
            match=re.escape(
                "Frozen classes can't use on_setattr "
                "(frozen-ness was inherited)."
            ),
        ):

            @attr.define(on_setattr=attr.setters.validate)
            class C(A):
                pass

    @pytest.mark.parametrize(
        "decorator",
        [
            partial(attr.s, frozen=True, slots=True, auto_exc=True),
            attr.frozen,
            attr.define,
            attr.mutable,
        ],
    )
    def test_discard_context(self, decorator):
        """
        raise from None works.

        Regression test for #703.
        """

        @decorator
        class MyException(Exception):
            x: str = attr.ib()

        with pytest.raises(MyException) as ei:
            try:
                raise ValueError()
            except ValueError:
                raise MyException("foo") from None

        assert "foo" == ei.value.x
        assert ei.value.__cause__ is None
