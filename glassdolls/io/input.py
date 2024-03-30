"""
Used for Player Input.
"""

import sys
from typing import Any, Sequence

import blessed
from attrs import define, field
from blessed.keyboard import Keystroke
from blinker import NamedSignal, signal

from glassdolls.io import logger
from glassdolls.constants import USER_MOVEMENT
from glassdolls.io.signals import SignalSender


@define
class UserInput(SignalSender):
    term: "blessed.Terminal"

    # Signals
    signal_user_input: NamedSignal = field(init=False, repr=False)
    signal_player_movement: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.signal_user_input = signal(f"{self.__class__.__name__}_user_input")
        self.signal_player_movement = signal(f"{self.__class__.__name__}_user_movement")

    def wait_for_key(
        self, available_user_key: Sequence[Keystroke] | Sequence[str] | None = None
    ) -> str:
        """
        Wait for user_input within the `available_user_key` possible values, send signal and return value.

        Notes
        -----
        See: https://blessed.readthedocs.io/en/latest/keyboard.html#keycodes

        Args:
            user_key (str | None, optional): Keycode for desired user key.  None will take any key. Defaults to None.
        """
        with self.term.cbreak():

            while True:
                val: Keystroke = self.term.inkey()

                if val is not None:
                    # If it's a sequence (like up arrow), take the key name.
                    # Make all key values upper for standardization.
                    key_value = val.upper() if not val.is_sequence else val.name.upper()
                    break

        logger.debug(f'USER INPUT: {val} ("{key_value}")')
        self.triage_user_input(key_value=key_value)
        return key_value

    def triage_user_input(self, key_value: str) -> None:
        if key_value in ["KEY_LEFT", "KEY_RIGHT", "KEY_DOWN", "KEY_UP"]:
            player_movement = USER_MOVEMENT[key_value]
            self.send_signal(
                self.signal_player_movement, data={"direction": player_movement}
            )
        elif key_value == "Q":
            sys.exit(0)
