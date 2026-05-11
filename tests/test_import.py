# SPDX-License-Identifier: MIT

import attr
import attrs


class TestImportStar:
    def test_from_attr_import_star(self):
        """
        import * from attr
        """
        # attr_import_star contains `from attr import *`, which cannot
        # be done here because *-imports are only allowed on module level.
        from . import attr_import_star  # noqa: F401


class TestDir:
    def test_attr_dir_includes_lazy_submodules(self):
        assert "converters" in dir(attr)
        assert "validators" in dir(attr)

    def test_attrs_dir_includes_lazy_submodules(self):
        assert "converters" in dir(attrs)
        assert "validators" in dir(attrs)
