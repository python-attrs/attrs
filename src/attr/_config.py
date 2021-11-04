from __future__ import absolute_import, division, print_function


__all__ = ["set_run_validators", "get_run_validators"]

_run_validators = True


def set_run_validators(run):
    """
    Set whether or not validators are run.  By default, they are run.

    .. deprecated:: 21.3.0 will not be moved to new ``attrs`` namespace.
        Use :func:`attr.validators.set_disabled()` instead.
    """
    if not isinstance(run, bool):
        raise TypeError("'run' must be bool.")
    global _run_validators
    _run_validators = run


def get_run_validators():
    """
    Return whether or not validators are run.

    .. deprecated:: 21.3.0 will not be moved to new ``attrs`` namespace.
        Use :func:`attr.validators.get_disabled()` instead.
    """
    return _run_validators
