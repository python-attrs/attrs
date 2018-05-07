"""
Tests for `attr._config`.
"""

from __future__ import absolute_import, division, print_function
from unittest.mock import patch

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

    def test_get(self):
        """
        Sets different settings in _config._config_data.
        """
        for prop in ('frozen_setattrs', 'frozen_delattrs'):
            assert _config.get(prop, False) == None

    def test_set(self):
        value = 'TEST VALUE'
        with patch.dict('attr._config._config_data'):
            for prop in ('frozen_setattrs', 'frozen_delattrs'):
                _config.set(prop, value)
                assert _config._config_data[prop] == value
