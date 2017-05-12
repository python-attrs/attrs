"""
Tests for behaviour of annotations on attributes.
"""

import attr

try:
    from typing import get_type_hints
except ImportError:
    def get_type_hints(x):
        return getattr(x, '__annotations__', {})


@attr.s()
class A(object):
    a = attr.ib(annotation=int)
    b = attr.ib()


@attr.s(init=False)
class B(object):
    a = attr.ib(annotation=int)
    b = attr.ib()

    def __init__(self, a, b):
        self.a = a
        self.b = b


class TestAnnotations(object):
    def test_propagates_annotations_to_attribute_object(self):
        assert A.a.annotation == int
        assert A.b.annotation == attr.NOTHING

    def test_propagates_annotation_to_init_if_requested(self):
        assert get_type_hints(A.__init__) == {'a': int}

    def test_does_not_annotate_init_if_not_generated(self):
        assert get_type_hints(B.__init__) == {}

    def test_correctly_annotates_even_without_init(self):
        assert B.a.annotation == int
        assert B.b.annotation == attr.NOTHING
