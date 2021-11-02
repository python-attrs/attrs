from __future__ import absolute_import, division, print_function

from contextlib import contextmanager


__all__ = ["set_run_validators", "get_run_validators"]

_run_validators = True


def set_run_validators(run):
    """
    Set whether or not validators are run.  By default, they are run.
    """
    if not isinstance(run, bool):
        raise TypeError("'run' must be bool.")
    global _run_validators
    _run_validators = run


def get_run_validators():
    """
    Return whether or not validators are run.
    """
    return _run_validators


@contextmanager
def no_run_validators():
    """
    Context manager that disables running validators within its context.

    .. versionadded:: 21.3.0
    """
    set_run_validators(False)
    try:
        yield
    finally:
        set_run_validators(True)
