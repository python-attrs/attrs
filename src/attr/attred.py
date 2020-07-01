from typing import Callable


def attred(**attrs):
    def inner(callabl: Callable):
        for attr_name, attr_value in attrs.items():
            setattr(callabl, attr_name, attr_value)
        return callabl

    return inner
