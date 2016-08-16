from __future__ import absolute_import, division, print_function


class FrozenInstanceError(AttributeError):
    """
    A frozen/immutable instance has been attempted to be modified.
    """
