"""
Tests for attr.converters
"""
from __future__ import absolute_import, division, print_function

import attr
from attr.converters import list_of, set_of, frozenset_of, from_dict


@attr.s
class MockAttrs(object):
    a = attr.ib()


class TestListOf(object):
    """
    Tests for `list_of`
    """
    def test_success(self):
        """
        Successfully create a list from an iterable of dicts
        """
        conv = list_of(MockAttrs)
        data = [{'a': 1},
                {'a': 2},
                {'a': 3}]
        assert conv(data) == [MockAttrs(a=1),
                              MockAttrs(a=2),
                              MockAttrs(a=3)]

    def test_repr(self):
        """
        Returned converter has a useful `__repr__`
        """
        conv = list_of(MockAttrs)
        assert ("<list_of converter for type {type!r}>"
                .format(type=MockAttrs)
                ) == repr(conv)


class TestSetOf(object):
    """
    Tests for `set_of`
    """
    def test_success(self):
        """
        Successfully create a set from an iterable of dicts
        """
        conv = set_of(MockAttrs)
        data = [{'a': 1},
                {'a': 2},
                {'a': 3}]
        assert conv(data) == set([MockAttrs(a=1),
                                  MockAttrs(a=2),
                                  MockAttrs(a=3)])

    def test_repr(self):
        """
        Returned converter has a useful `__repr__`
        """
        conv = set_of(MockAttrs)
        assert ("<set_of converter for type {type!r}>"
                .format(type=MockAttrs)
                ) == repr(conv)


class TestFrozensetOf(object):
    """
    Tests for `frozenset_of`
    """
    def test_success(self):
        """
        Successfully create a set from an iterable of dicts
        """
        conv = frozenset_of(MockAttrs)
        data = [{'a': 1},
                {'a': 2},
                {'a': 3}]
        assert conv(data) == frozenset([MockAttrs(a=1),
                                        MockAttrs(a=2),
                                        MockAttrs(a=3)])

    def test_repr(self):
        """
        Returned converter has a useful `__repr__`
        """
        conv = frozenset_of(MockAttrs)
        assert ("<frozenset_of converter for type {type!r}>"
                .format(type=MockAttrs)
                ) == repr(conv)


class TestFromDict(object):
    """
    Tests for `from_dict`
    """
    def test_success(self):
        """
        Successfully create an instance from a dict
        """
        conv = from_dict(MockAttrs)
        data = {'a': 1}
        assert conv(data) == MockAttrs(a=1)

    def test_repr(self):
        """
        Returned converter has a useful `__repr__`
        """
        conv = from_dict(MockAttrs)
        assert ("<from_dict converter for type {type!r}>"
                .format(type=MockAttrs)
                ) == repr(conv)
