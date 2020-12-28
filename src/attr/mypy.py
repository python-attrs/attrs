from typing import Callable, Optional

from mypy.plugin import ClassDefContext, Plugin
from mypy.typeops import TypingType


def plugin(version: str) -> "TypingType[Plugin]":
    """
    `version` is the mypy version string

    We might want to use this to print a warning if the mypy version
    being used is newer, or especially older, than we expect (or need).
    """
    return AttrsPlugin


class AttrsPlugin(Plugin):
    def get_class_decorator_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        return None
