"""
Tests for behavior specific to forward references via PEP 749.
"""

from attrs import define, fields, resolve_types


def test_forward_class_reference():
    """
    Class A can reference B even though it is defined later.
    """

    @define
    class A:
        b: B

    class B:
        pass

    resolve_types(A)

    assert fields(A).b.type is B
