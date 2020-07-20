"""
End-to-end tests.
"""

from __future__ import absolute_import, division, print_function

import pickle

from copy import deepcopy

import pytest
import six

from hypothesis import assume, given
from hypothesis.strategies import booleans

import attr

from attr import setters
from attr._compat import PY2, TYPE
from attr._make import NOTHING, Attribute
from attr.exceptions import FrozenAttributeError, FrozenInstanceError
from attr.validators import instance_of, matches_re

from .strategies import optional_bool


@attr.s
class C1(object):
    x = attr.ib(validator=attr.validators.instance_of(int))
    y = attr.ib()


@attr.s(slots=True)
class C1Slots(object):
    x = attr.ib(validator=attr.validators.instance_of(int))
    y = attr.ib()


foo = None


@attr.s()
class C2(object):
    x = attr.ib(default=foo)
    y = attr.ib(default=attr.Factory(list))


@attr.s(slots=True)
class C2Slots(object):
    x = attr.ib(default=foo)
    y = attr.ib(default=attr.Factory(list))


@attr.s
class Base(object):
    x = attr.ib()

    def meth(self):
        return self.x


@attr.s(slots=True)
class BaseSlots(object):
    x = attr.ib()

    def meth(self):
        return self.x


@attr.s
class Sub(Base):
    y = attr.ib()


@attr.s(slots=True)
class SubSlots(BaseSlots):
    y = attr.ib()


@attr.s(frozen=True, slots=True)
class Frozen(object):
    x = attr.ib()


@attr.s
class SubFrozen(Frozen):
    y = attr.ib()


@attr.s(frozen=True, slots=False)
class FrozenNoSlots(object):
    x = attr.ib()


class Meta(type):
    pass


@attr.s
@six.add_metaclass(Meta)
class WithMeta(object):
    pass


@attr.s(slots=True)
@six.add_metaclass(Meta)
class WithMetaSlots(object):
    pass


FromMakeClass = attr.make_class("FromMakeClass", ["x"])


class TestDarkMagic(object):
    """
    Integration tests.
    """

    @pytest.mark.parametrize("cls", [C2, C2Slots])
    def test_fields(self, cls):
        """
        `attr.fields` works.
        """
        assert (
            Attribute(
                name="x",
                default=foo,
                validator=None,
                repr=True,
                cmp=None,
                eq=True,
                order=True,
                hash=None,
                init=True,
                inherited=False,
            ),
            Attribute(
                name="y",
                default=attr.Factory(list),
                validator=None,
                repr=True,
                cmp=None,
                eq=True,
                order=True,
                hash=None,
                init=True,
                inherited=False,
            ),
        ) == attr.fields(cls)

    @pytest.mark.parametrize("cls", [C1, C1Slots])
    def test_asdict(self, cls):
        """
        `attr.asdict` works.
        """
        assert {"x": 1, "y": 2} == attr.asdict(cls(x=1, y=2))

    @pytest.mark.parametrize("cls", [C1, C1Slots])
    def test_validator(self, cls):
        """
        `instance_of` raises `TypeError` on type mismatch.
        """
        with pytest.raises(TypeError) as e:
            cls("1", 2)

        # Using C1 explicitly, since slotted classes don't support this.
        assert (
            "'x' must be <{type} 'int'> (got '1' that is a <{type} "
            "'str'>).".format(type=TYPE),
            attr.fields(C1).x,
            int,
            "1",
        ) == e.value.args

    @given(booleans())
    def test_renaming(self, slots):
        """
        Private members are renamed but only in `__init__`.
        """

        @attr.s(slots=slots)
        class C3(object):
            _x = attr.ib()

        assert "C3(_x=1)" == repr(C3(x=1))

    @given(booleans(), booleans())
    def test_programmatic(self, slots, frozen):
        """
        `attr.make_class` works.
        """
        PC = attr.make_class("PC", ["a", "b"], slots=slots, frozen=frozen)

        assert (
            Attribute(
                name="a",
                default=NOTHING,
                validator=None,
                repr=True,
                cmp=None,
                eq=True,
                order=True,
                hash=None,
                init=True,
                inherited=False,
            ),
            Attribute(
                name="b",
                default=NOTHING,
                validator=None,
                repr=True,
                cmp=None,
                eq=True,
                order=True,
                hash=None,
                init=True,
                inherited=False,
            ),
        ) == attr.fields(PC)

    @pytest.mark.parametrize("cls", [Sub, SubSlots])
    def test_subclassing_with_extra_attrs(self, cls):
        """
        Subclassing (where the subclass has extra attrs) does what you'd hope
        for.
        """
        obj = object()
        i = cls(x=obj, y=2)
        assert i.x is i.meth() is obj
        assert i.y == 2
        if cls is Sub:
            assert "Sub(x={obj}, y=2)".format(obj=obj) == repr(i)
        else:
            assert "SubSlots(x={obj}, y=2)".format(obj=obj) == repr(i)

    @pytest.mark.parametrize("base", [Base, BaseSlots])
    def test_subclass_without_extra_attrs(self, base):
        """
        Subclassing (where the subclass does not have extra attrs) still
        behaves the same as a subclass with extra attrs.
        """

        class Sub2(base):
            pass

        obj = object()
        i = Sub2(x=obj)
        assert i.x is i.meth() is obj
        assert "Sub2(x={obj})".format(obj=obj) == repr(i)

    @pytest.mark.parametrize(
        "frozen_class",
        [
            Frozen,  # has slots=True
            attr.make_class("FrozenToo", ["x"], slots=False, frozen=True),
        ],
    )
    def test_frozen_instance(self, frozen_class):
        """
        Frozen instances can't be modified (easily).
        """
        frozen = frozen_class(1)

        with pytest.raises(FrozenInstanceError) as e:
            frozen.x = 2

        with pytest.raises(FrozenInstanceError) as e:
            del frozen.x

        assert e.value.args[0] == "can't set attribute"
        assert 1 == frozen.x

    @pytest.mark.parametrize(
        "cls",
        [
            C1,
            C1Slots,
            C2,
            C2Slots,
            Base,
            BaseSlots,
            Sub,
            SubSlots,
            Frozen,
            FrozenNoSlots,
            FromMakeClass,
        ],
    )
    @pytest.mark.parametrize("protocol", range(2, pickle.HIGHEST_PROTOCOL + 1))
    def test_pickle_attributes(self, cls, protocol):
        """
        Pickling/un-pickling of Attribute instances works.
        """
        for attribute in attr.fields(cls):
            assert attribute == pickle.loads(pickle.dumps(attribute, protocol))

    @pytest.mark.parametrize(
        "cls",
        [
            C1,
            C1Slots,
            C2,
            C2Slots,
            Base,
            BaseSlots,
            Sub,
            SubSlots,
            Frozen,
            FrozenNoSlots,
            FromMakeClass,
        ],
    )
    @pytest.mark.parametrize("protocol", range(2, pickle.HIGHEST_PROTOCOL + 1))
    def test_pickle_object(self, cls, protocol):
        """
        Pickle object serialization works on all kinds of attrs classes.
        """
        if len(attr.fields(cls)) == 2:
            obj = cls(123, 456)
        else:
            obj = cls(123)
        assert repr(obj) == repr(pickle.loads(pickle.dumps(obj, protocol)))

    def test_subclassing_frozen_gives_frozen(self):
        """
        The frozen-ness of classes is inherited.  Subclasses of frozen classes
        are also frozen and can be instantiated.
        """
        i = SubFrozen("foo", "bar")

        assert i.x == "foo"
        assert i.y == "bar"

    @pytest.mark.parametrize("cls", [WithMeta, WithMetaSlots])
    def test_metaclass_preserved(self, cls):
        """
        Metaclass data is preserved.
        """
        assert Meta == type(cls)

    def test_default_decorator(self):
        """
        Default decorator sets the default and the respective method gets
        called.
        """

        @attr.s
        class C(object):
            x = attr.ib(default=1)
            y = attr.ib()

            @y.default
            def compute(self):
                return self.x + 1

        assert C(1, 2) == C()

    @pytest.mark.parametrize("slots", [True, False])
    @pytest.mark.parametrize("frozen", [True, False])
    @pytest.mark.parametrize("weakref_slot", [True, False])
    def test_attrib_overwrite(self, slots, frozen, weakref_slot):
        """
        Subclasses can overwrite attributes of their base class.
        """

        @attr.s(slots=slots, frozen=frozen, weakref_slot=weakref_slot)
        class SubOverwrite(Base):
            x = attr.ib(default=attr.Factory(list))

        assert SubOverwrite([]) == SubOverwrite()

    def test_dict_patch_class(self):
        """
        dict-classes are never replaced.
        """

        class C(object):
            x = attr.ib()

        C_new = attr.s(C)

        assert C_new is C

    def test_hash_by_id(self):
        """
        With dict classes, hashing by ID is active for hash=False even on
        Python 3.  This is incorrect behavior but we have to retain it for
        backward compatibility.
        """

        @attr.s(hash=False)
        class HashByIDBackwardCompat(object):
            x = attr.ib()

        assert hash(HashByIDBackwardCompat(1)) != hash(
            HashByIDBackwardCompat(1)
        )

        @attr.s(hash=False, eq=False)
        class HashByID(object):
            x = attr.ib()

        assert hash(HashByID(1)) != hash(HashByID(1))

        @attr.s(hash=True)
        class HashByValues(object):
            x = attr.ib()

        assert hash(HashByValues(1)) == hash(HashByValues(1))

    def test_handles_different_defaults(self):
        """
        Unhashable defaults + subclassing values work.
        """

        @attr.s
        class Unhashable(object):
            pass

        @attr.s
        class C(object):
            x = attr.ib(default=Unhashable())

        @attr.s
        class D(C):
            pass

    @pytest.mark.parametrize("slots", [True, False])
    def test_hash_false_eq_false(self, slots):
        """
        hash=False and eq=False make a class hashable by ID.
        """

        @attr.s(hash=False, eq=False, slots=slots)
        class C(object):
            pass

        assert hash(C()) != hash(C())

    @pytest.mark.parametrize("slots", [True, False])
    def test_eq_false(self, slots):
        """
        eq=False makes a class hashable by ID.
        """

        @attr.s(eq=False, slots=slots)
        class C(object):
            pass

        assert hash(C()) != hash(C())

    def test_overwrite_base(self):
        """
        Base classes can overwrite each other and the attributes are added
        in the order they are defined.
        """

        @attr.s
        class C(object):
            c = attr.ib(default=100)
            x = attr.ib(default=1)
            b = attr.ib(default=23)

        @attr.s
        class D(C):
            a = attr.ib(default=42)
            x = attr.ib(default=2)
            d = attr.ib(default=3.14)

        @attr.s
        class E(D):
            y = attr.ib(default=3)
            z = attr.ib(default=4)

        assert "E(c=100, b=23, a=42, x=2, d=3.14, y=3, z=4)" == repr(E())

    @pytest.mark.parametrize("base_slots", [True, False])
    @pytest.mark.parametrize("sub_slots", [True, False])
    @pytest.mark.parametrize("base_frozen", [True, False])
    @pytest.mark.parametrize("sub_frozen", [True, False])
    @pytest.mark.parametrize("base_weakref_slot", [True, False])
    @pytest.mark.parametrize("sub_weakref_slot", [True, False])
    @pytest.mark.parametrize("base_converter", [True, False])
    @pytest.mark.parametrize("sub_converter", [True, False])
    def test_frozen_slots_combo(
        self,
        base_slots,
        sub_slots,
        base_frozen,
        sub_frozen,
        base_weakref_slot,
        sub_weakref_slot,
        base_converter,
        sub_converter,
    ):
        """
        A class with a single attribute, inheriting from another class
        with a single attribute.
        """

        @attr.s(
            frozen=base_frozen,
            slots=base_slots,
            weakref_slot=base_weakref_slot,
        )
        class Base(object):
            a = attr.ib(converter=int if base_converter else None)

        @attr.s(
            frozen=sub_frozen, slots=sub_slots, weakref_slot=sub_weakref_slot
        )
        class Sub(Base):
            b = attr.ib(converter=int if sub_converter else None)

        i = Sub("1", "2")

        assert i.a == (1 if base_converter else "1")
        assert i.b == (2 if sub_converter else "2")

        if base_frozen or sub_frozen:
            with pytest.raises(FrozenInstanceError):
                i.a = "2"

            with pytest.raises(FrozenInstanceError):
                i.b = "3"

    def test_tuple_class_aliasing(self):
        """
        itemgetter and property are legal attribute names.
        """

        @attr.s
        class C(object):
            property = attr.ib()
            itemgetter = attr.ib()
            x = attr.ib()

        assert "property" == attr.fields(C).property.name
        assert "itemgetter" == attr.fields(C).itemgetter.name
        assert "x" == attr.fields(C).x.name

    @pytest.mark.parametrize("slots", [True, False])
    @pytest.mark.parametrize("frozen", [True, False])
    def test_auto_exc(self, slots, frozen):
        """
        Classes with auto_exc=True have a Exception-style __str__, compare and
        hash by id, and store the fields additionally in self.args.
        """

        @attr.s(auto_exc=True, slots=slots, frozen=frozen)
        class FooError(Exception):
            x = attr.ib()
            y = attr.ib(init=False, default=42)
            z = attr.ib(init=False)
            a = attr.ib()

        FooErrorMade = attr.make_class(
            "FooErrorMade",
            bases=(Exception,),
            attrs={
                "x": attr.ib(),
                "y": attr.ib(init=False, default=42),
                "z": attr.ib(init=False),
                "a": attr.ib(),
            },
            auto_exc=True,
            slots=slots,
            frozen=frozen,
        )

        assert FooError(1, "foo") != FooError(1, "foo")
        assert FooErrorMade(1, "foo") != FooErrorMade(1, "foo")

        for cls in (FooError, FooErrorMade):
            with pytest.raises(cls) as ei1:
                raise cls(1, "foo")

            with pytest.raises(cls) as ei2:
                raise cls(1, "foo")

            e1 = ei1.value
            e2 = ei2.value

            assert e1 is e1
            assert e1 == e1
            assert e2 == e2
            assert e1 != e2
            assert "(1, 'foo')" == str(e1) == str(e2)
            assert (1, "foo") == e1.args == e2.args

            hash(e1) == hash(e1)
            hash(e2) == hash(e2)

            if not frozen:
                deepcopy(e1)
                deepcopy(e2)

    @pytest.mark.parametrize("slots", [True, False])
    @pytest.mark.parametrize("frozen", [True, False])
    def test_auto_exc_one_attrib(self, slots, frozen):
        """
        Having one attribute works with auto_exc=True.

        Easy to get wrong with tuple literals.
        """

        @attr.s(auto_exc=True, slots=slots, frozen=frozen)
        class FooError(Exception):
            x = attr.ib()

        FooError(1)

    @pytest.mark.parametrize("slots", [True, False])
    @pytest.mark.parametrize("frozen", [True, False])
    def test_eq_only(self, slots, frozen):
        """
        Classes with order=False cannot be ordered.

        Python 3 throws a TypeError, in Python2 we have to check for the
        absence.
        """

        @attr.s(eq=True, order=False, slots=slots, frozen=frozen)
        class C(object):
            x = attr.ib()

        if not PY2:
            possible_errors = (
                "unorderable types: C() < C()",
                "'<' not supported between instances of 'C' and 'C'",
                "unorderable types: C < C",  # old PyPy 3
            )

            with pytest.raises(TypeError) as ei:
                C(5) < C(6)

            assert ei.value.args[0] in possible_errors
        else:
            i = C(42)
            for m in ("lt", "le", "gt", "ge"):
                assert None is getattr(i, "__%s__" % (m,), None)

    @given(cmp=optional_bool, eq=optional_bool, order=optional_bool)
    def test_cmp_deprecated_attribute(self, cmp, eq, order):
        """
        Accessing Attribute.cmp raises a deprecation warning but returns True
        if cmp is True, or eq and order are *both* effectively True.
        """
        # These cases are invalid and raise a ValueError.
        assume(cmp is None or (eq is None and order is None))
        assume(not (eq is False and order is True))

        if cmp is not None:
            rv = cmp
        elif eq is True or eq is None:
            rv = order is None or order is True
        elif cmp is None and eq is None and order is None:
            rv = True
        elif cmp is None or eq is None:
            rv = False
        else:
            pytest.fail(
                "Unexpected state: cmp=%r eq=%r order=%r" % (cmp, eq, order)
            )

        with pytest.deprecated_call() as dc:

            @attr.s
            class C(object):
                x = attr.ib(cmp=cmp, eq=eq, order=order)

            assert rv == attr.fields(C).x.cmp

        if cmp is not None:
            # Remove warning from creating the attribute if cmp is not None.
            dc.pop()

        (w,) = dc.list

        assert (
            "The usage of `cmp` is deprecated and will be removed on or after "
            "2021-06-01.  Please use `eq` and `order` instead."
            == w.message.args[0]
        )


class TestSetAttr(object):
    def test_change(self):
        """
        The return value of a hook overwrites the value. But they are not run
        on __init__.
        """

        def hook(*a, **kw):
            return "hooked!"

        @attr.s
        class Hooked(object):
            x = attr.ib(on_setattr=hook)
            y = attr.ib()

        h = Hooked("x", "y")

        assert "x" == h.x
        assert "y" == h.y

        h.x = "xxx"
        h.y = "yyy"

        assert "yyy" == h.y
        assert "hooked!" == h.x

    def test_frozen_attribute(self):
        """
        Frozen attributes raise FrozenAttributeError, others are not affected.
        """

        @attr.s
        class PartiallyFrozen(object):
            x = attr.ib(on_setattr=setters.frozen)
            y = attr.ib()

        pf = PartiallyFrozen("x", "y")

        pf.y = "yyy"

        assert "yyy" == pf.y

        with pytest.raises(FrozenAttributeError):
            pf.x = "xxx"

        assert "x" == pf.x

    @pytest.mark.parametrize(
        "on_setattr",
        [setters.validate, [setters.validate], setters.pipe(setters.validate)],
    )
    def test_validator(self, on_setattr):
        """
        Validators are run and they don't alter the value.
        """

        @attr.s(on_setattr=on_setattr)
        class ValidatedAttribute(object):
            x = attr.ib()
            y = attr.ib(validator=[instance_of(str), matches_re("foo.*qux")])

        va = ValidatedAttribute(42, "foobarqux")

        with pytest.raises(TypeError) as ei:
            va.y = 42

        assert "foobarqux" == va.y

        assert ei.value.args[0].startswith("'y' must be <")

        with pytest.raises(ValueError) as ei:
            va.y = "quxbarfoo"

        assert ei.value.args[0].startswith("'y' must match regex '")

        assert "foobarqux" == va.y

        va.y = "foobazqux"

        assert "foobazqux" == va.y

    def test_pipe(self):
        """
        Multiple hooks are possible, in that case the last return value is
        used. They can be supplied using the pipe functions or by passing a
        list to on_setattr.
        """

        s = [setters.convert, lambda _, __, nv: nv + 1]

        @attr.s
        class Piped(object):
            x1 = attr.ib(converter=int, on_setattr=setters.pipe(*s))
            x2 = attr.ib(converter=int, on_setattr=s)

        p = Piped("41", "22")

        assert 41 == p.x1
        assert 22 == p.x2

        p.x1 = "41"
        p.x2 = "22"

        assert 42 == p.x1
        assert 23 == p.x2

    def test_make_class(self):
        """
        on_setattr of make_class gets forwarded.
        """
        C = attr.make_class("C", {"x": attr.ib()}, on_setattr=setters.frozen)

        c = C(1)

        with pytest.raises(FrozenAttributeError):
            c.x = 2

    def test_no_validator_no_converter(self):
        """
        validate and convert tolerate missing validators and converters.
        """

        @attr.s(on_setattr=[setters.convert, setters.validate])
        class C(object):
            x = attr.ib()

        c = C(1)

        c.x = 2

    def test_validate_respects_run_validators_config(self):
        """
        If run validators is off, validate doesn't run them.
        """

        @attr.s(on_setattr=setters.validate)
        class C(object):
            x = attr.ib(validator=attr.validators.instance_of(int))

        c = C(1)

        attr.set_run_validators(False)

        c.x = "1"

        assert "1" == c.x

        attr.set_run_validators(True)

        with pytest.raises(TypeError) as ei:
            c.x = "1"

        assert ei.value.args[0].startswith("'x' must be <")

    def test_frozen_on_setattr_class_is_caught(self):
        """
        @attr.s(on_setattr=X, frozen=True) raises an ValueError.
        """
        with pytest.raises(ValueError) as ei:

            @attr.s(frozen=True, on_setattr=setters.validate)
            class C(object):
                x = attr.ib()

        assert "Frozen classes can't use on_setattr." == ei.value.args[0]

    def test_frozen_on_setattr_attribute_is_caught(self):
        """
        attr.ib(on_setattr=X) on a frozen class raises an ValueError.
        """

        with pytest.raises(ValueError) as ei:

            @attr.s(frozen=True)
            class C(object):
                x = attr.ib(on_setattr=setters.validate)

        assert "Frozen classes can't use on_setattr." == ei.value.args[0]
