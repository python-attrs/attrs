"""
Tests for `attr.validators`.
"""

from __future__ import absolute_import, division, print_function

import pytest
import zope.interface

from attr._compat import TYPE
from attr.validators import instance_of, provides, optional, chain, guess_type_from_validators, is_mandatory
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


class TestChain(object):
    """
    Tests for `chain`.
    """
    def test_success_with_type(self):
        """
        Nothing happens if types match.
        """
        v = chain(instance_of(int))
        v(None, simple_attr("test"), 42)

    def test_fail(self):
        """
        Raises `TypeError` on wrong types.
        """
        v = chain(instance_of(int))
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
        v = chain(instance_of(int))
        assert (
            ("<validator sequence : (<instance_of validator for type "
             "<{type} 'int'>>,)>")
            .format(type=TYPE)
        ) == repr(v)


class TestIsMandatory(object):
    """
    Tests for utility method `is_mandatory`.
    """
    def test_simple(self):
        """
        if validator is a simple instance_of it works
        """
        att = simple_attr("test", validator=instance_of(int))
        assert is_mandatory(att) == True

    def test_optional(self):
        """
        if validator is an optional containing is_instance it works
        """
        att = simple_attr("test", validator=optional(instance_of(int)))
        assert is_mandatory(att) == False


def custom_validator(instance, attribute, value):
    allowed = {'+', '*'}
    if value not in allowed:
        raise ValueError('\'op\' has to be a string in ' + str(allowed) + '!')


class TestGuessType(object):
    """
    Tests for utility method `guess_type_from_validators`
    """

    def test_simple(self):
        """
        if validator is a simple instance_of it works
        """
        att = simple_attr("test", validator=instance_of(int))
        assert guess_type_from_validators(att) == int

    def test_simple_not_found(self):
        """
        if validator is a simple instance_of it works
        """
        att = simple_attr("test", validator=custom_validator)
        assert guess_type_from_validators(att) == None

    def test_optional(self):
        """
        if validator is an optional containing is_instance it works
        """
        att = simple_attr("test", validator=optional(instance_of(int)))
        assert guess_type_from_validators(att) == int

    def test_optional_not_found(self):
        """
        if validator is a simple instance_of it works
        """
        att = simple_attr("test", validator=optional(custom_validator))
        assert guess_type_from_validators(att) == None

    def test_chain(self):
        """
        if validator is a chain containing is_instance it also works
        """
        att = simple_attr("test", validator=chain(custom_validator, instance_of(str)))
        assert guess_type_from_validators(att) == str

    def test_chain_not_found(self):
        """
        if validator is a chain containing is_instance it also works
        """
        att = simple_attr("test", validator=chain(custom_validator, custom_validator))
        assert guess_type_from_validators(att) == None

    def test_optional_chain(self):
        """
        if validator is an optional containing a chain containing an is_instance it also works
        """
        att = simple_attr("test", validator=optional(chain(custom_validator, instance_of(str))))
        assert guess_type_from_validators(att) == str

    def test_optional_chain_not_found(self):
        """
        if validator is an optional containing a chain containing an is_instance it also works
        """
        att = simple_attr("test", validator=optional(chain(custom_validator, custom_validator)))
        assert guess_type_from_validators(att) == None
