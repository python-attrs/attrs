"""
Tests for `attr._config`.
"""

from __future__ import absolute_import, division, print_function

import pytest

from attr import _config


class TestConfig(object):
    def test_default(self):
        """
        Run validators by default.
        """
        assert True is _config._run_validators

    def test_set_run_validators(self):
        """
        Sets `_run_validators`.
        """
        _config.set_run_validators(False)
        assert False is _config._run_validators
        _config.set_run_validators(True)
        assert True is _config._run_validators

    def test_get_run_validators(self):
        """
        Returns `_run_validators`.
        """
        _config._run_validators = False
        assert _config._run_validators is _config.get_run_validators()
        _config._run_validators = True
        assert _config._run_validators is _config.get_run_validators()

    def test_wrong_type(self):
        """
        Passing anything else than a boolean raises TypeError.
        """
        with pytest.raises(TypeError) as e:
            _config.set_run_validators("False")
        assert "'run' must be bool." == e.value.args[0]

    def test_no_run_validators(self):
        """
        The `no_run_validators` context manager disables running validators,
        but only within its context.
        """
        assert _config._run_validators is True
        with _config.no_run_validators():
            assert _config._run_validators is False
        assert _config._run_validators is True

    def test_no_run_validators_with_errors(self):
        """
        Running validators is re-enabled even if an error is raised.
        """
        assert _config._run_validators is True
        with pytest.raises(ValueError):
            with _config.no_run_validators():
                assert _config._run_validators is False
                raise ValueError("haha!")
        assert _config._run_validators is True
