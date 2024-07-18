"""
Benchmark attrs using CodSpeed.
"""

from __future__ import annotations

import os

import pytest

import attrs


if os.environ.get("CODSPEED_ENV") is None:
    pytest.skip("Not running in CodSpeed environment", allow_module_level=True)

pytestmark = pytest.mark.benchmark()

ROUNDS = 1_000


def test_create_simple_class():
    """
    Benchmark creating and instantiating a simple class without any extras.
    """
    for _ in range(ROUNDS):

        @attrs.define
        class LocalC:
            x: int
            y: str
            z: dict[str, int]

        LocalC(1, "2", {})


def test_create_simple_class_make_class():
    """
    Benchmark creating and instantiating a simple class using attrs.make_class().
    """
    for i in range(ROUNDS):
        C = attrs.make_class(
            f"C{i}",
            {
                "x": attrs.field(type=int),
                "y": attrs.field(type=str),
                "z": attrs.field(type=dict[str, int]),
            },
        )

        C(1, "2", {})


@attrs.define
class C:
    x: int = 0
    y: str = "foo"
    z: dict[str, int] = attrs.Factory(dict)


def test_instantiate_no_defaults():
    """
    Benchmark instantiating a class without using any defaults.
    """
    for _ in range(ROUNDS):
        C(1, "2", {})


def test_instantiate_with_defaults():
    """
    Benchmark instantiating a class relying on defaults.
    """
    for _ in range(ROUNDS):
        C()


def test_eq_equal():
    """
    Benchmark comparing two equal instances for equality.
    """
    c1 = C()
    c2 = C()

    for _ in range(ROUNDS):
        c1 == c2


def test_eq_unequal():
    """
    Benchmark comparing two unequal instances for equality.
    """
    c1 = C()
    c2 = C(1, "bar", {"baz": 42})

    for _ in range(ROUNDS):
        c1 == c2


@attrs.frozen
class HashableC:
    x: int = 0
    y: str = "foo"
    z: tuple[str] = ("bar",)


def test_hash():
    """
    Benchmark hashing an instance.
    """
    c = HashableC()

    for _ in range(ROUNDS):
        hash(c)
