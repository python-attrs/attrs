# SPDX-License-Identifier: MIT

import pytest

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

    def test_from_attrs_import_star(self):
        """
        import * from attrs
        """
        # attrs_import_star contains `from attrs import *`, which cannot
        # be done here because *-imports are only allowed on module level.
        from . import attrs_import_star  # noqa: F401


class TestDir:
    def test_attr_dir_includes_lazy_submodules(self):
        """
        converters and validators are listed in dir(attr).
        """
        assert "converters" in dir(attr)
        assert "validators" in dir(attr)
        assert "__name__" in dir(attr)
        assert "_make_getattr" in dir(attr)

    def test_attrs_dir_includes_lazy_submodules(self):
        """
        converters and validators are listed in dir(attrs).
        """
        assert "converters" in dir(attrs)
        assert "validators" in dir(attrs)
        assert "__name__" in dir(attrs)
        assert "_make_getattr" in dir(attrs)


class TestAll:
    @pytest.mark.parametrize("mod", [attr, attrs], ids=["attr", "attrs"])
    def test_all_entries_exist(self, mod):
        """
        Every name in __all__ resolves to a real attribute.
        """
        missing = [name for name in mod.__all__ if not hasattr(mod, name)]

        assert [] == missing
