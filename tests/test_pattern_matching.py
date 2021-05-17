# flake8: noqa
# Python 3.10 issue in flake8 : https://github.com/PyCQA/pyflakes/issues/634
import pytest

import attr

from attr._make import make_class


class TestPatternMatching(object):
    """
    Pattern matching syntax test cases.
    """

    def test_simple_match_case(self):
        """
        Simple match case statement
        """

        @attr.s()
        class C(object):
            a = attr.ib()

        assert C.__match_args__ == ("a",)

        matched = False
        c = C(a=1)
        match c:
            case C(a):
                matched = True

        assert matched

    def test_explicit_match_args(self):
        """
        Manually set empty __match_args__ will not match.
        """

        ma = ()

        @attr.s()
        class C(object):
            a = attr.ib()
            __match_args__ = ma

        c = C(a=1)

        msg = r"C\(\) accepts 0 positional sub-patterns \(1 given\)"
        with pytest.raises(TypeError, match=msg):
            match c:
                case C(a):
                    pass

    def test_match_args_kw_only(self):
        """
        kw_only being set doesn't generate __match_args__
        kw_only field is not included in __match_args__
        """

        @attr.s()
        class C(object):
            a = attr.ib(kw_only=True)
            b = attr.ib()

        assert C.__match_args__ == ("b",)

        c = C(a=1, b=1)
        msg = r"C\(\) accepts 1 positional sub-pattern \(2 given\)"
        with pytest.raises(TypeError, match=msg):
            match c:
                case C(a, b):
                    pass

        found = False
        match c:
            case C(b, a=a):
                found = True

        assert found

        @attr.s(match_args=True, kw_only=True)
        class C(object):
            a = attr.ib()
            b = attr.ib()

        c = C(a=1, b=1)
        msg = r"C\(\) accepts 0 positional sub-patterns \(2 given\)"
        with pytest.raises(TypeError, match=msg):
            match c:
                case C(a, b):
                    pass

        found = False
        match c:
            case C(a=a, b=b):
                found = True

        assert found
