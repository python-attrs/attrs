from typing import Callable


def attred(**attrs):
    """
    Takes any number of keyword arguments and applies those key-values to
    decorated callable

    .. versionadded:: 20.1.0
    """

    def inner(callabl: Callable):
        for attr_name, attr_value in attrs.items():
            setattr(callabl, attr_name, attr_value)
        return callabl

    return inner
