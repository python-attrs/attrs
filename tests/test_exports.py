# SPDX-License-Identifier: MIT

import attr
import attrs


def test_all_exports_resolve():
    """Every name in __all__ resolves on both attr and attrs."""
    for mod in (attr, attrs):
        for name in mod.__all__:
            try:
                assert hasattr(mod, name), f"{mod.__name__}.__all__ lists missing {name!r}"
            except ValueError:
                if name != "__version_info__":
                    raise
