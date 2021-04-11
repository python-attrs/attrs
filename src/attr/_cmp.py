from __future__ import absolute_import, division, print_function

import functools

from ._make import _make_ne, attrib, attrs


_operation_names = {"eq": "==", "lt": "<", "le": "<=", "gt": ">", "ge": ">="}


def cmp_using(
    eq=None,
    lt=None,
    le=None,
    gt=None,
    ge=None,
    require_same_type=True,
    class_name=None,
):
    """
    Utility function that creates a class with customized equality and
    ordering methods.

    The resulting class will have a full set of ordering methods if
    at least one of ``{lt, le, gt, ge}`` and ``eq``  are provided.

    :param Optional[callable] eq: `callable` used to evaluate equality
        of two objects.
    :param Optional[callable] lt: `callable` used to evaluate whether
        one object is less than another object.
    :param Optional[callable] le: `callable` used to evaluate whether
        one object is less than or equal to another object.
    :param Optional[callable] gt: `callable` used to evaluate whether
        one object is greater than another object.
    :param Optional[callable] ge: `callable` used to evaluate whether
        one object is greater than or equal to another object.

    :param bool require_same_type: When `True`, equality and ordering methods
        will return `NotImplemented` if objects are not of the same type.

    :param Optional[str] class_name: Name of class. Defaults to 'Comparable'.

    .. versionadded:: 21.1.0
    """

    @attrs(slots=True, eq=False, order=False)
    class Comparable(object):
        value = attrib()
        _requirements = []

        def _is_comparable_to(self, other):
            """
            Check whether `other` is comparable to `self`.
            """
            for func in self._requirements:
                if not func(self, other):
                    return False
            return True

    if class_name is None:
        Comparable.__qualname__ = Comparable.__name__
    else:
        Comparable.__name__ = class_name
        Comparable.__qualname__ = class_name

    # Add same type requirement.
    if require_same_type:
        Comparable._requirements.append(_check_same_type)

    # Add operations.
    num_order_fucntions = 0
    has_eq_function = False

    if eq is not None:
        has_eq_function = True
        Comparable.__eq__ = _make_operator("eq", eq)
        Comparable.__ne__ = _make_ne()

    if lt is not None:
        num_order_fucntions += 1
        Comparable.__lt__ = _make_operator("lt", lt)

    if le is not None:
        num_order_fucntions += 1
        Comparable.__le__ = _make_operator("le", le)

    if gt is not None:
        num_order_fucntions += 1
        Comparable.__gt__ = _make_operator("gt", gt)

    if ge is not None:
        num_order_fucntions += 1
        Comparable.__ge__ = _make_operator("ge", ge)

    # Add total ordering if at least one operation was defined.
    if 0 < num_order_fucntions < 4:
        if not has_eq_function:
            # functools.total_ordering requires __eq__ to be defined,
            # so raise early error here to keep a nice stach.
            raise ValueError(
                "eq must be define is order to complete ordering from "
                "lt, le, gt, ge."
            )
        Comparable = functools.total_ordering(Comparable)

    # Fix dunders to add nice qualified names, etc.
    for name in ["__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__"]:
        method = getattr(Comparable, name, None)
        if method is not None:
            setattr(Comparable, name, _add_method_dunders(Comparable, method))

    return Comparable


def _add_method_dunders(cls, method):
    """
    Add __module__ and __qualname__ to a *method* if possible.
    """
    try:
        method.__module__ = cls.__module__
    except AttributeError:
        pass

    try:
        method.__qualname__ = ".".join((cls.__qualname__, method.__name__))
    except AttributeError:
        pass

    return method


def _make_operator(name, func):
    """
    Create operator method.
    """

    def method(self, other):
        """
        Evaluate operator and either return the result or NotImplemented.
        """
        if not self._is_comparable_to(other):
            return NotImplemented

        result = func(self.value, other.value)
        if result is NotImplemented:
            return NotImplemented

        return result

    method.__name__ = "__%s__" % (name,)
    method.__doc__ = "Return a %s b.  Computed by attrs." % (
        _operation_names[name],
    )

    return method


def _check_same_type(self, other):
    """
    Return True if *self* and *other* are of the same type, False otherwise.
    """
    return other.value.__class__ is self.value.__class__
