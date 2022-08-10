# SPDX-License-Identifier: MIT

import json
import os.path
import shutil
import subprocess

import pytest

import attr


_found_pyright = shutil.which("pyright")
pytestmark = pytest.mark.skipif(not _found_pyright, reason="Requires pyright.")


@attr.s(frozen=True)
class PyrightDiagnostic:
    severity = attr.ib()
    message = attr.ib()


def parse_pyright_output(test_file):
    pyright = subprocess.run(
        ["pyright", "--outputjson", str(test_file)], capture_output=True
    )
    pyright_result = json.loads(pyright.stdout)

    diagnostics = {
        PyrightDiagnostic(d["severity"], d["message"])
        for d in pyright_result["generalDiagnostics"]
    }

    return diagnostics


def test_pyright_baseline():
    """The __dataclass_transform__ decorator allows pyright to determine
    attrs decorated class types.
    """
    diagnostics = parse_pyright_output(
        os.path.dirname(__file__) + "/dataclass_transform_example.py"
    )

    # Expected diagnostics as per pyright 1.1.135
    expected_diagnostics = {
        PyrightDiagnostic(
            severity="information",
            message='Type of "Define.__init__" is'
            ' "(self: Define, a: str, b: int) -> None"',
        ),
        PyrightDiagnostic(
            severity="information",
            message='Type of "DefineConverter.__init__" is '
            '"(self: DefineConverter, with_converter: int) -> None"',
        ),
        PyrightDiagnostic(
            severity="information",
            message='Type of "d.a" is "Literal[\'new\']"',
        ),
        PyrightDiagnostic(
            severity="error",
            message='Cannot assign member "a" for type '
            '"FrozenDefine"\n\xa0\xa0"FrozenDefine" is frozen',
        ),
        PyrightDiagnostic(
            severity="information",
            message='Type of "d2.a" is "Literal[\'new\']"',
        ),
    }

    assert diagnostics == expected_diagnostics


def test_pyright_attrsinstance_is_any(tmp_path):
    """
    Test that `AttrsInstance` is `Any` under Pyright.
    """
    test_pyright_attrsinstance_is_any_path = (
        tmp_path / "test_pyright_attrsinstance_is_any.py"
    )
    test_pyright_attrsinstance_is_any_path.write_text(
        """\
import attrs

reveal_type(attrs.AttrsInstance)
"""
    )

    diagnostics = parse_pyright_output(test_pyright_attrsinstance_is_any_path)
    expected_diagnostics = {
        PyrightDiagnostic(
            severity="information",
            message='Type of "attrs.AttrsInstance" is "Any"',
        ),
    }
    assert diagnostics == expected_diagnostics
