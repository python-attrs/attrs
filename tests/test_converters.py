"""
Tests for `attr.converters`.
"""

from __future__ import absolute_import

import sys

from datetime import datetime, timedelta, timezone
from distutils.util import strtobool

import pytest

import attr

from attr import Factory, attrib
from attr.converters import (
    default_if_none,
    optional,
    pipe,
    to_attrs,
    to_dt,
    to_iterable,
    to_mapping,
    to_tuple,
    to_union,
)


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


class TestDefaultIfNone(object):
    def test_missing_default(self):
        """
        Raises TypeError if neither default nor factory have been passed.
        """
        with pytest.raises(TypeError, match="Must pass either"):
            default_if_none()

    def test_too_many_defaults(self):
        """
        Raises TypeError if both default and factory are passed.
        """
        with pytest.raises(TypeError, match="but not both"):
            default_if_none(True, lambda: 42)

    def test_factory_takes_self(self):
        """
        Raises ValueError if passed Factory has takes_self=True.
        """
        with pytest.raises(ValueError, match="takes_self"):
            default_if_none(Factory(list, takes_self=True))

    @pytest.mark.parametrize("val", [1, 0, True, False, "foo", "", object()])
    def test_not_none(self, val):
        """
        If a non-None value is passed, it's handed down.
        """
        c = default_if_none("nope")

        assert val == c(val)

        c = default_if_none(factory=list)

        assert val == c(val)

    def test_none_value(self):
        """
        Default values are returned when a None is passed.
        """
        c = default_if_none(42)

        assert 42 == c(None)

    def test_none_factory(self):
        """
        Factories are used if None is passed.
        """
        c = default_if_none(factory=list)

        assert [] == c(None)

        c = default_if_none(default=Factory(list))

        assert [] == c(None)


class TestToAttrs:
    """Tests for to_attrs()."""

    def test_from_data(self):
        """
        Dicts can be converted to class instances.
        """

        @attr.s
        class C:
            x = attr.ib()
            y = attr.ib()

        converter = to_attrs(C)
        assert converter({"x": 2, "y": 3}) == C(2, 3)

    def test_from_inst(self):
        """
        Existing instances remain unchanged.
        """

        @attr.s
        class C:
            x = attr.ib()
            y = attr.ib()

        inst = C(2, 3)
        converter = to_attrs(C)
        assert converter(inst) is inst

    @pytest.mark.skipif(
        sys.version_info < (3, 6),
        reason="__init_subclass__ is not yet supported",
    )
    def test_from_dict_factory(self):
        """
        Classes can specify a "from_dict" factory that will be called.
        """

        @attr.s
        class Animal:
            type = attr.ib()
            __classes__ = {}

            def __init_subclass__(cls, **kwargs):
                super().__init_subclass__(**kwargs)
                cls.__classes__[cls.__name__] = cls

            @classmethod
            def from_dict(cls, **attribs):
                cls_name = attribs["type"]
                return cls.__classes__[cls_name](**attribs)

        @attr.s(kw_only=True)
        class Cat(Animal):
            x = attr.ib()

        @attr.s(kw_only=True)
        class Dog(Animal):
            x = attr.ib()
            y = attr.ib(default=3)

        converter = to_attrs(Animal)
        assert converter({"type": "Cat", "x": 2}) == Cat(type="Cat", x=2)
        assert converter({"type": "Dog", "x": 2}) == Dog(type="Dog", x=2, y=3)

    def test_invalid_cls(self):
        """
        Raise TypeError when neither a dict nor an instance of the class is
        passed.
        """

        @attr.s
        class C:
            x = attr.ib()
            y = attr.ib()

        converter = to_attrs(C)
        with pytest.raises(TypeError):
            converter([2, 3])


class TestToDt:
    """Tests for to_dt()."""

    def test_from_dt(self):
        """
        Existing datetimes are returned unchanged.
        """
        dt = datetime(2020, 5, 4, 13, 37)
        result = to_dt(dt)
        assert result is dt

    @pytest.mark.parametrize(
        "input, expected",
        [
            ("2020-05-04 13:37:00", datetime(2020, 5, 4, 13, 37)),
            ("2020-05-04T13:37:00", datetime(2020, 5, 4, 13, 37)),
            # (
            #     "2020-05-04T13:37:00Z",
            #     datetime(2020, 5, 4, 13, 37, tzinfo=timezone.utc)),
            # ),
            (
                "2020-05-04T13:37:00+00:00",
                datetime(2020, 5, 4, 13, 37, tzinfo=timezone.utc),
            ),
            (
                "2020-05-04T13:37:00+02:00",
                datetime(
                    2020,
                    5,
                    4,
                    13,
                    37,
                    tzinfo=timezone(timedelta(seconds=7200)),
                ),
            ),
        ],
    )
    def test_from_str(self, input, expected):
        """
        Existing datetimes are returned unchanged.
        """
        result = to_dt(input)
        assert result == expected

    def test_invalid_input(self):
        """
        Invalid inputs raises a TypeError.
        """
        with pytest.raises(TypeError):
            to_dt(3)


class TestToIterable:
    """Tests for to_iterable()."""

    @pytest.mark.parametrize("cls", [list, set, tuple])
    def test_to_iterable(self, cls):
        """
        An iterable's data and the iterable itself can be converted to
        different types.
        """
        converter = to_iterable(cls, int)
        assert converter(["1", "2", "3"]) == cls([1, 2, 3])


class TestToTuple:
    """Tests for to_tuple()."""

    @pytest.mark.parametrize("cls", [tuple])
    def test_to_tuple(self, cls):
        """
        Struct-like tuples can contain different data types.
        """
        converter = to_tuple(cls, [int, float, str])
        assert converter(["1", "2.2", "s"]) == cls([1, 2.2, "s"])

    @pytest.mark.parametrize("val", [["1", "2.2", "s"], ["1"]])
    def test_tuple_wrong_input_length(self, val):
        """
        Input data must have exactly as many elements as the tuple definition
        has converters.
        """
        converter = to_tuple(tuple, [int, float])
        with pytest.raises(
            TypeError,
            match="Value must have 2 items but has: {}".format(len(val)),
        ):
            converter(val)


class TestToMapping:
    """Tests for to_mapping()."""

    @pytest.mark.parametrize("cls", [dict])
    def test_to_dict(self, cls):
        """
        Keys and values of dicts can be converted to (different) types.
        """
        converter = to_mapping(cls, int, float)
        assert converter({"1": "2", "2": "2.5"}) == cls([(1, 2.0), (2, 2.5)])


class TestToUnion:
    """Tests for to_union()."""

    @pytest.mark.parametrize(
        "types, val, expected_type, expected_val",
        [
            ([type(None), int], None, type(None), None),
            ([type(None), int], "3", int, 3),
            ([int, float], "3", int, 3),
            ([int, float], 3.2, float, 3.2),  # Do not cast 3.2 to int!
            ([int, float], "3.2", float, 3.2),
            ([int, float, str], "3.2s", str, "3.2s"),
            ([int, float, bool, str], "3.2", str, "3.2"),
            ([int, float, bool, str], True, bool, True),
            ([int, float, bool, str], "True", str, "True"),
            ([int, float, bool, str], "", str, ""),
        ],
    )
    def test_to_union(self, types, val, expected_type, expected_val):
        """
        Union data is converted to the first matching type.  If the input data
        already has a valid type, it is returned without conversion.  For
        example, floats will not be converted to ints when the type is
        "Union[int, float]".
        """
        converter = to_union(types)
        result = converter(val)
        assert type(result) is expected_type
        assert result == expected_val


class TestPipe(object):
    def test_success(self):
        """
        Succeeds if all wrapped converters succeed.
        """
        c = pipe(str, strtobool, bool)

        assert True is c("True") is c(True)

    def test_fail(self):
        """
        Fails if any wrapped converter fails.
        """
        c = pipe(str, strtobool)

        # First wrapped converter fails:
        with pytest.raises(ValueError):
            c(33)

        # Last wrapped converter fails:
        with pytest.raises(ValueError):
            c("33")

    def test_sugar(self):
        """
        `pipe(c1, c2, c3)` and `[c1, c2, c3]` are equivalent.
        """

        @attr.s
        class C(object):
            a1 = attrib(default="True", converter=pipe(str, strtobool, bool))
            a2 = attrib(default=True, converter=[str, strtobool, bool])

        c = C()
        assert True is c.a1 is c.a2
