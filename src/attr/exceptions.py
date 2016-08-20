from __future__ import absolute_import, division, print_function


class FrozenInstanceError(AttributeError):
    """
    A frozen/immutable instance has been attempted to be modified.

    It mirrors the behavior of ``namedtuples`` by using the same error message
    and subclassing :exc:`AttributeError``.
    """
    msg = "can't set attribute"
    args = [msg]
