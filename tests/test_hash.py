"""
Tests for our hashing functionality.
"""
import pytest

import attr

from hypothesis import given
from hypothesis.strategies import booleans


@given(slots=booleans(), frozen=booleans(), cmp=booleans())
def test_no_subclass_no_hash(slots, frozen, cmp):
    """
    Classes inheriting from ``object``, and setting ``hash=False`` fall back
    to ``object.__hash__``.
    """
    @attr.s(hash=False, slots=slots, frozen=frozen, cmp=cmp)
    class A(object):
        a = attr.ib()

    assert A.__hash__ is object.__hash__
    hash(A(1))  # Should not raise.

    assert hash(A(1)) != hash(A(1))   # Identity-based hash.


@given(slots=booleans(), frozen=booleans(), cmp=booleans())
def test_no_subclass_has_hash(slots, frozen, cmp):
    """
    Classes inheriting from ``object``, and setting ``hash=True`` use the
    ``attrs``-generated hash.
    """
    @attr.s(hash=True, slots=slots, frozen=frozen, cmp=cmp)
    class A(object):
        a = attr.ib()

    assert A.__hash__ is not object.__hash__
    hash(A(1))   # Should not raise.

    assert hash(A(1)) == hash(A(1))


@given(slots=booleans(), frozen=booleans(), cmp=booleans())
def test_no_subclass_default_hash(slots, frozen, cmp):
    """
    Classes inheriting from ``object``, and setting ``hash=None`` set their
    ``__hash__`` according to whether they're frozen and comparable.
    """
    @attr.s(slots=slots, frozen=frozen, cmp=cmp)
    class A(object):
        a = attr.ib()

    if frozen and cmp:
        assert A.__hash__ is not object.__hash__
        hash(A(1))   # Should not raise.

        assert hash(A(1)) == hash(A(1))
    elif cmp and not frozen:
        # We make the class unhashable.
        assert A.__hash__ is None

        with pytest.raises(TypeError):
            hash(A(1))
    elif not cmp:
        # Fall back to object.__hash__.
        assert A.__hash__ is object.__hash__
        hash(A(1))  # Should not raise.

        assert hash(A(1)) != hash(A(1))   # Identity-based hash.


@given(super_slots=booleans(), super_frozen=booleans(), slots=booleans(),
       frozen=booleans())
def test_subclass_default_hash(super_slots, super_frozen, slots, frozen):
    """
    ``cmp=False`` and ``hash=None`` makes classes use the ``__hash__`` of their
    superclass.
    """
    @attr.s(slots=super_slots, frozen=super_frozen)
    class A(object):
        a = attr.ib()

    @attr.s(slots=slots, frozen=frozen, cmp=False)
    class B(A):
        b = attr.ib()

    assert B.__hash__ is A.__hash__
