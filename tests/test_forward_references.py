# SPDX-License-Identifier: MIT

"""
Tests for behavior specific to forward references via PEP 649 / 749.

Collected only on Python 3.14+ (see conftest.py).
"""

import inspect
import sys

import annotationlib
import pytest

from attrs import define, field, fields, resolve_types


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


def test_generated_init_matches_handwritten_forward_ref(slots):
    """
    Generated ``__init__`` annotations resolve late forward references like a
    hand-written constructor (issue #1596, no ``from __future__ import
    annotations``).
    """

    class Works:
        def __init__(self, foo: Foo) -> None:
            self._foo = foo

    @define(slots=slots)
    class DoesNotWork:
        _foo: Foo

    class Foo:
        pass

    assert inspect.signature(Works) == inspect.signature(DoesNotWork)
    assert (
        annotationlib.get_annotations(
            DoesNotWork.__init__, format=annotationlib.Format.VALUE
        )["foo"]
        is Foo
    )
    # Live module globals (not a creation-time snapshot).
    assert (
        DoesNotWork.__init__.__globals__
        is sys.modules[DoesNotWork.__module__].__dict__
    )
    assert DoesNotWork.__init__.__annotate__ is not None
    # Runtime still constructs.
    assert DoesNotWork(Foo())._foo.__class__ is Foo


def test_generated_init_annotate_uses_slotted_class(slots):
    """
    ``__annotate__`` closes over the final class, including after slots rewrite.
    """

    @define(slots=slots)
    class C:
        _x: X

    class X:
        pass

    annotate = C.__init__.__annotate__
    assert annotate is not None
    anns = annotate(annotationlib.Format.VALUE)
    assert anns["x"] is X
    # Cell rewrite must point at the class users actually subclass / isinstance.
    found_cls = False
    for cell in annotate.__closure__ or ():
        try:
            contents = cell.cell_contents
        except ValueError:
            continue
        if contents is C:
            found_cls = True
            break
    assert found_cls


def test_converter_annotation_remains_static():
    """
    Converter first-parameter types stay on the generated init (not re-fetched
    from the field annotation).
    """

    def to_int(value: str) -> int:
        return int(value)

    @define
    class C:
        x: int = field(converter=to_int)

    anns = annotationlib.get_annotations(
        C.__init__, format=annotationlib.Format.VALUE
    )
    assert anns["x"] is str
    assert C("5").x == 5
