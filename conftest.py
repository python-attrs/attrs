from __future__ import absolute_import, division, print_function

import sys

from hypothesis import HealthCheck, settings


def pytest_configure(config):
    # HealthCheck.too_slow causes more trouble than good -- especially in CIs.
    settings.register_profile(
        "patience", settings(suppress_health_check=[HealthCheck.too_slow])
    )
    settings.load_profile("patience")


collect_ignore = []
if sys.version_info[:2] < (3, 6):
    collect_ignore.extend(
        [
            "tests/test_annotations.py",
            "tests/test_init_subclass.py",
            "tests/test_next_gen.py",
        ]
    )
