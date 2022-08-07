# SPDX-License-Identifier: MIT

from hypothesis import HealthCheck, settings

from attr._compat import PY310


def pytest_configure(config):
    # HealthCheck.too_slow causes more trouble than good -- especially in CIs.
    settings.register_profile(
        "patience", settings(suppress_health_check=[HealthCheck.too_slow])
    )
    settings.load_profile("patience")


collect_ignore = []
if not PY310:
    collect_ignore.extend(["tests/test_pattern_matching.py"])
