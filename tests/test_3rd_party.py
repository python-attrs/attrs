# SPDX-License-Identifier: MIT

"""
Tests for compatibility against other Python modules.
"""

import pytest

from hypothesis import given

from attr._compat import PY_3_14_PLUS

from .strategies import simple_classes


cloudpickle = pytest.importorskip("cloudpickle")


@pytest.mark.xfail(
    PY_3_14_PLUS, reason="cloudpickle is currently broken on 3.14."
)
class TestCloudpickleCompat:
    """
    Tests for compatibility with ``cloudpickle``.
    """

    @given(simple_classes(cached_property=False))
    def test_repr(self, cls):
        """
        attrs instances can be pickled and un-pickled with cloudpickle.
        """
        inst = cls()
        # Exact values aren't a concern so long as neither direction
        # raises an exception.
        pkl = cloudpickle.dumps(inst)
        cloudpickle.loads(pkl)
