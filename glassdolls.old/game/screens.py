from typing import Sequence
from enum import Enum, auto

import glassdolls

from blessed import Terminal
from blessed.keyboard import Keystroke


class ScreenTypes(Enum):
    """Screen Types (used for possible user inputs)."""

    STORY = auto()
    INPUT = auto()
    MAP = auto()


class ScreenRenderer:
    def __init__(self, term: Terminal) -> None:
        self.term = term

    def render(self, screens: Sequence["glassdolls.game.components.Widget"]) -> None:
        """Render the screens in ``screens`` on the Terminal."""
        self.refresh()
        for screen in screens:
            screen.display()

    def render_and_wait_for_key(
        self,
        screens: Sequence["glassdolls.game.components.Widget"],
        user_key: str | None = None,
    ) -> Keystroke:
        """
        Render and wait for user key.

        Helper method combining ``.render`` and ``.wait_for_key``.
        """
        self.render(screens=screens)
        return self.wait_for_key(user_key=user_key)

    def refresh(self) -> None:
        print(f"{self.term.home}{self.term.clear}")

    def wait_for_key(self, user_key: str | None = None) -> Keystroke:
        """
        Wait for user_input with value ``key``.

        Notes
        -----
        See: https://blessed.readthedocs.io/en/latest/keyboard.html#keycodes

        Args:
            user_key (str | None, optional): Keycode for desired user key.  None will take any key. Defaults to None.
        """
        with self.term.cbreak():
            while True:
                val = self.term.inkey()
                if val.is_sequence and ((user_key is None) or (val.name == user_key)):
                    break
        return val
