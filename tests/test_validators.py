"""
Tests for `attr.validators`.
"""

from __future__ import absolute_import, division, print_function

import pytest
import zope.interface

from attr.validators import instance_of, provides, optional, composite
from attr._compat import TYPE

from .utils import simple_attr


class TestInstanceOf(object):
    """
    Tests for `instance_of`.
    """
    def test_success(self):
        """
        Nothing happens if types match.
        """
        v = instance_of(int)
        v(None, simple_attr("test"), 42)

    def test_subclass(self):
        """
        Subclasses are accepted too.
        """
        v = instance_of(int)
        # yep, bools are a subclass of int :(
        v(None, simple_attr("test"), True)

    def test_fail(self):
        """
        Raises `TypeError` on wrong types.
        """
        v = instance_of(int)
        a = simple_attr("test")
        with pytest.raises(TypeError) as e:
            v(None, a, "42")
        assert (
            "'test' must be <{type} 'int'> (got '42' that is a <{type} "
            "'str'>).".format(type=TYPE),
            a, int, "42",

        ) == e.value.args

    def test_repr(self):
        """
        Returned validator has a useful `__repr__`.
        """
        v = instance_of(int)
        assert (
            "<instance_of validator for type <{type} 'int'>>"
            .format(type=TYPE)
        ) == repr(v)


class IFoo(zope.interface.Interface):
    """
    An interface.
    """
    def f():
        """
        A function called f.
        """


class TestProvides(object):
    """
    Tests for `provides`.
    """
    def test_success(self):
        """
        Nothing happens if value provides requested interface.
        """
        @zope.interface.implementer(IFoo)
        class C(object):
            def f(self):
                pass

        v = provides(IFoo)
        v(None, simple_attr("x"), C())

    def test_fail(self):
        """
        Raises `TypeError` if interfaces isn't provided by value.
        """
        value = object()
        a = simple_attr("x")

        v = provides(IFoo)
        with pytest.raises(TypeError) as e:
            v(None, a, value)
        assert (
            "'x' must provide {interface!r} which {value!r} doesn't."
            .format(interface=IFoo, value=value),
            a, IFoo, value,
        ) == e.value.args

    def test_repr(self):
        """
        Returned validator has a useful `__repr__`.
        """
        v = provides(IFoo)
        assert (
            "<provides validator for interface {interface!r}>"
            .format(interface=IFoo)
        ) == repr(v)


class TestOptional(object):
    """
    Tests for `optional`.
    """
    def test_success_with_type(self):
        """
        Nothing happens if types match.
        """
        v = optional(instance_of(int))
        v(None, simple_attr("test"), 42)

    def test_success_with_none(self):
        """
        Nothing happens if None.
        """
        v = optional(instance_of(int))
        v(None, simple_attr("test"), None)

    def test_fail(self):
        """
        Raises `TypeError` on wrong types.
        """
        v = optional(instance_of(int))
        a = simple_attr("test")
        with pytest.raises(TypeError) as e:
            v(None, a, "42")
        assert (
            "'test' must be <{type} 'int'> (got '42' that is a <{type} "
            "'str'>).".format(type=TYPE),
            a, int, "42",

        ) == e.value.args

    def test_repr(self):
        """
        Returned validator has a useful `__repr__`.
        """
        v = optional(instance_of(int))
        assert (
            ("<optional validator for <instance_of validator for type "
             "<{type} 'int'>> or None>")
            .format(type=TYPE)
        ) == repr(v)


class TestComposite(object):
    """
    Tests for `composite`.
    """
    def test_requires_at_least_two_validators(self):
        """
        Calling with less than two validators raises TypeError.
        """
        with pytest.raises(TypeError):
            composite()

        with pytest.raises(TypeError):
            composite(instance_of(int))

        composite(instance_of(int), instance_of(str))

    def test_success(self):
        def test_validator(inst, attr, value):
            if value != "test":
                raise ValueError("Test error")
        v = composite(instance_of(str), test_validator)
        v(None, simple_attr("test"), "test")

    def test_fail(self):
        def test_validator(inst, attr, value):
            if value != "test":
                raise ValueError("Test error")
        v = composite(instance_of(str), test_validator)

        with pytest.raises(ValueError):
            v(None, simple_attr("test"), "not test")
        with pytest.raises(TypeError):
            v(None, simple_attr("test"), 42)

    def test_repr(self):
        """
        Returned validator has a useful `__repr__`.
        """
        def test_validator(inst, attr, value):
            if value != "test":
                raise ValueError("Test error")
        v = composite(instance_of(str), test_validator)
        assert (
            "<composite validator for validators {!r}>"
            .format(v.validators)
        ) == repr(v)
