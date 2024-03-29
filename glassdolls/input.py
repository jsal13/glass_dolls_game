"""
Used for Player Input.
"""

from attrs import define, field
from blessed.keyboard import Keystroke


@define
class UserInput:
    keypress: Keystroke
    _key: str = field(init=False)

    def __attrs_post_init__(self) -> None:
        self._key = self.keypress.lower()
