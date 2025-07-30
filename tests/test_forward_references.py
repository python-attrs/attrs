"""
Tests for behavior specific to forward references via PEP 749.
"""

from attrs import define


def test_forward_class_reference():
    """
    Class A can reference B even though it is defined later.
    """

    @define
    class A:
        b: B

    class B:
        pass
