from __future__ import absolute_import

from attr import *  # noqa: F401,F403


# This is imported by test_import::test_import_attr_star; this must
# be done indirectly because importing * is only allowed on module level,
# so can't be done inside a test.
