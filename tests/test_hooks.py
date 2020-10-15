import functools
import json

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Type, Union

import pytest

import attr

from attr.hooks import auto_convert, auto_serialize
from attr.validators import le


auto_converter = functools.partial(attr.frozen, field_transformer=auto_convert)


class TestTransformHook:
    """
    Tests for `attrs(tranform_value_serializer=func)`
    """

    def test_hook_applied(self):
        """
        The transform hook is applied to all attributes.  Types can be missing,
        explicitly set, or annotated.
        """
        results = []

        def hook(cls, attribs):
            results[:] = [(a.name, a.type) for a in attribs]
            return attribs

        @attr.s(field_transformer=hook)
        class C:
            x = attr.ib()
            y = attr.ib(type=int)
            z: float = attr.ib()

        assert results == [("x", None), ("y", int), ("z", float)]

    def test_hook_applied_auto_attrib(self):
        """
        The transform hook is applied to all attributes and type annotations
        are detected.
        """
        results = []

        def hook(cls, attribs):
            results[:] = [(a.name, a.type) for a in attribs]
            return attribs

        @attr.s(auto_attribs=True, field_transformer=hook)
        class C:
            x: int
            y: str = attr.ib()

        assert results == [("x", int), ("y", str)]

    def test_hook_applied_modify_attrib(self):
        """
        The transform hook can modify attributes.
        """

        def hook(cls, attribs):
            return [a.assoc(converter=a.type) for a in attribs]

        @attr.s(auto_attribs=True, field_transformer=hook)
        class C:
            x: int = attr.ib(converter=int)
            y: float

        c = C(x="3", y="3.14")
        assert c == C(x=3, y=3.14)

    def test_hook_remove_field(self):
        """
        It is possible to remove fields via the hook.
        """

        def hook(cls, attribs):
            return [a for a in attribs if a.type is not int]

        @attr.s(auto_attribs=True, field_transformer=hook)
        class C:
            x: int
            y: float

        assert attr.asdict(C(2.7)) == {"y": 2.7}

    def test_hook_add_field(self):
        """
        It is possible to add fields via the hook.
        """

        def hook(cls, attribs):
            a1 = attribs[0]
            a2 = a1.assoc(name="new")
            return [a1, a2]

        @attr.s(auto_attribs=True, field_transformer=hook)
        class C:
            x: int

        assert attr.asdict(C(1, 2)) == {"x": 1, "new": 2}

    def test_hook_with_inheritance(self):
        """
        The hook receives all fields from base classes.
        """

        def hook(cls, attribs):
            assert [a.name for a in attribs] == ["x", "y"]
            # Remove Base' "x"
            return attribs[1:]

        @attr.s(auto_attribs=True)
        class Base:
            x: int

        @attr.s(auto_attribs=True, field_transformer=hook)
        class Sub(Base):
            y: int

        assert attr.asdict(Sub(2)) == {"y": 2}


class TestAsDictHook:
    def test_asdict(self):
        """
        asdict() calls the hooks in attrs classes and in other datastructures
        like lists or dicts.
        """

        def hook(inst, a, v):
            if isinstance(v, datetime):
                return v.isoformat()
            return v

        @attr.dataclass
        class Child:
            x: datetime
            y: List[datetime]

        @attr.dataclass
        class Parent:
            a: Child
            b: List[Child]
            c: Dict[str, Child]
            d: Dict[str, datetime]

        inst = Parent(
            a=Child(1, [datetime(2020, 7, 1)]),
            b=[Child(2, [datetime(2020, 7, 2)])],
            c={"spam": Child(3, [datetime(2020, 7, 3)])},
            d={"eggs": datetime(2020, 7, 4)},
        )

        result = attr.asdict(inst, value_serializer=hook)
        assert result == {
            "a": {"x": 1, "y": ["2020-07-01T00:00:00"]},
            "b": [{"x": 2, "y": ["2020-07-02T00:00:00"]}],
            "c": {"spam": {"x": 3, "y": ["2020-07-03T00:00:00"]}},
            "d": {"eggs": "2020-07-04T00:00:00"},
        }

    def test_asdict_calls(self):
        """
        The correct instances and attribute names are passed to the hook.
        """
        calls = []

        def hook(inst, a, v):
            calls.append((inst, a.name if a else a, v))
            return v

        @attr.dataclass
        class Child:
            x: int

        @attr.dataclass
        class Parent:
            a: Child
            b: List[Child]
            c: Dict[str, Child]

        inst = Parent(a=Child(1), b=[Child(2)], c={"spam": Child(3)})

        attr.asdict(inst, value_serializer=hook)
        assert calls == [
            (inst, "a", inst.a),
            (inst.a, "x", inst.a.x),
            (inst, "b", inst.b),
            (inst.b[0], "x", inst.b[0].x),
            (inst, "c", inst.c),
            (None, None, "spam"),
            (inst.c["spam"], "x", inst.c["spam"].x),
        ]


class LeEnum(Enum):
    spam = "Le spam"
    eggs = "Le eggs"


@auto_converter
class Child:
    x: int = attr.ib()
    y: int = attr.ib(converter=float)


@auto_converter(kw_only=True)
class Parent:
    child: Child
    a: float
    b: float = attr.field(default=3.14, validator=le(2))
    c: LeEnum
    d: datetime
    e: "List[Child]"
    f: Set[datetime]


class TestAutoConvertHook:
    """Tests for the bundled auto-convert hook."""

    DATA = {
        "a": "1",
        "b": "2",
        "c": "Le spam",
        "d": "2020-05-04T13:37:00",
        "e": [{"x": "23", "y": "42"}],
        "f": ["2020-05-04T13:37:00", "2020-05-04T13:37:00"],
        "child": {"x": "23", "y": "42"},
    }

    @pytest.fixture(scope="class")
    def parent(self):
        return Parent(**self.DATA)

    def test_convert_to_parent(self, parent):
        """
        The auto_convert hook must convert attrs classes, datetimes, enums and
        basic type as well as basic containers.
        """
        assert parent == Parent(
            a=1.0,
            b=2.0,
            c=LeEnum.spam,
            d=datetime(2020, 5, 4, 13, 37),
            e=[Child(23, 42)],
            f={datetime(2020, 5, 4, 13, 37)},
            child=Child(23, 42),
        )

    def test_serialize_from_parent(self, parent):
        """
        The serialize_hook must be able to serialize the same types as the
        auto_convert hook.  The set with duplicate entries of attrib "f" is
        not the same as in the original dict!
        """
        d = attr.asdict(parent, value_serializer=auto_serialize)
        assert d == {
            "a": 1.0,
            "b": 2.0,
            "c": "Le spam",
            "d": "2020-05-04T13:37:00",
            "e": [{"x": 23, "y": 42}],
            "f": ["2020-05-04T13:37:00"],
            "child": {"x": 23, "y": 42},
        }

    def test_json_roundtrip(self, parent):
        """
        The roundtrip "inst -> JSON -> inst" must result in the same inst.
        """
        d = attr.asdict(parent, value_serializer=auto_serialize)
        assert Parent(**json.loads(json.dumps(d))) == parent

    def test_convert_to_struct_tuple(self):
        """
        Tuples can be defined like structs.
        """

        @auto_converter
        class C:
            x: Tuple[int, float, str]

        c = C(["3", "3.2", "3.2"])
        assert c.x == (3, 3.2, "3.2")

    def test_convert_to_iterable_tuple(self):
        """
        Tuples can be defined like (immutable) lists.
        """

        @auto_converter
        class C:
            x: Tuple[int, ...]

        c = C(["3", "2", "1"])
        assert c.x == (3, 2, 1)

    def test_to_mapping(self):
        """
        Converters are applied to dict keys and values.
        """

        @auto_converter
        class C:
            x: Dict[int, float]

        c = C({"1": "2"})
        assert c.x == {1: 2.0}

    @pytest.mark.parametrize("val, expected", [({}, None), ({"x": "2"}, 2)])
    def test_convert_to_optional(self, val, expected):
        """
        Conversion to Optional works with and without a value.
        """

        @auto_converter
        class C:
            x: Optional[int] = None

        c = C(**val)
        assert c.x == expected
        assert type(c.x) is type(expected)

    def test_convert_to_union(self):
        """
        Union values resolve to the first matching type
        """

        @auto_converter
        class C:
            x: Union[int, float]

        c = C(**{"x": "3.2"})
        assert c.x == 3.2
        assert type(c.x) is float

    def test_invalid_generic_type(self):
        """
        Annotating a generic type that the converter doesn't know leads to
        a TypeError.
        """
        with pytest.raises(
            TypeError, match="Cannot create converter for generic type:"
        ):

            @auto_converter
            class C:
                x: Type[int]

    def test_nested_conversion(self):
        """
        Generics (like lists and dicts) can be nested and will still be
        properly converted.
        """

        @auto_converter
        class A:
            x: int
            y: int

        @auto_converter
        class C:
            x: Dict[Tuple[int, int], List[Dict[int, A]]]

        c = C(
            {
                ("1", "2"): [
                    {"3": {"x": "4", "y": "5"}},
                    {"6": {"x": "7", "y": "8"}},
                ],
            }
        )
        assert c.x == {(1, 2): [{3: A(4, 5)}, {6: A(7, 8)}]}
