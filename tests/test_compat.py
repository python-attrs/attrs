# SPDX-License-Identifier: MIT

import types

from typing import Protocol

import pytest

import attr

from attr._compat import _IS_GENERATOR_RESULTS, _lazy_is_generator


@pytest.fixture(name="mp")
def _mp():
    return types.MappingProxyType({"x": 42, "y": "foo"})


class TestMetadataProxy:
    """
    Ensure properties of metadata proxy independently of hypothesis strategies.
    """

    def test_repr(self, mp):
        """
        repr makes sense and is consistent across Python versions.
        """
        assert any(
            [
                "mappingproxy({'x': 42, 'y': 'foo'})" == repr(mp),
                "mappingproxy({'y': 'foo', 'x': 42})" == repr(mp),
            ]
        )

    def test_immutable(self, mp):
        """
        All mutating methods raise errors.
        """
        with pytest.raises(TypeError, match="not support item assignment"):
            mp["z"] = 23

        with pytest.raises(TypeError, match="not support item deletion"):
            del mp["x"]

        with pytest.raises(AttributeError, match="no attribute 'update'"):
            mp.update({})

        with pytest.raises(AttributeError, match="no attribute 'clear'"):
            mp.clear()

        with pytest.raises(AttributeError, match="no attribute 'pop'"):
            mp.pop("x")

        with pytest.raises(AttributeError, match="no attribute 'popitem'"):
            mp.popitem()

        with pytest.raises(AttributeError, match="no attribute 'setdefault'"):
            mp.setdefault("x")


def test_attrsinstance_subclass_protocol():
    """
    It's possible to subclass AttrsInstance and Protocol at once.
    """

    class Foo(attr.AttrsInstance, Protocol):
        def attribute(self) -> int: ...


class TestLazyIsGenerator:
    def test_is_generator(self):
        """
        Returns True for generator functions and caches the result.
        """

        def gen():
            yield 1

        assert _lazy_is_generator(gen)()
        assert _IS_GENERATOR_RESULTS[gen] is True

    def test_is_not_generator(self):
        """
        Returns False for non-generator functions and caches the result.
        """

        def non_gen():
            return 1

        assert not _lazy_is_generator(non_gen)()
        assert _IS_GENERATOR_RESULTS[non_gen] is False

    def test_not_hashable(self):
        """
        If the user somehow manages to create a non-hashable function,
        the result is not hashed but the result is correct.
        """
        non_hashable = {}

        assert not _lazy_is_generator(non_hashable)()
