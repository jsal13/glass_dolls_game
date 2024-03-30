"""
Used for Player Input.
"""

import sys
from typing import Any, Sequence

import blessed
from attrs import define, field
from blessed.keyboard import Keystroke
from blinker import NamedSignal, signal

from glassdolls import logger
from glassdolls.constants import USER_MOVEMENT
from glassdolls.signals import SignalSender


@define
class UserInput(SignalSender):
    term: "blessed.Terminal"

    # Signals
    signal_user_input: NamedSignal = field(init=False, repr=False)
    signal_player_movement: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.signal_user_input = signal(f"{self.__class__.__name__}_user_input")
        self.signal_user_input.connect(self.handle_signal_user_input)

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
            key_value: str

            while True:
                val = self.term.inkey()

                if val is not None:
                    if val.is_sequence:
                        if val.name is None:
                            raise ValueError("Key value for {val} is 'None'.")
                        key_value = val.name
                        break
                    elif val:
                        key_value = str(val)
                        break
        logger.debug(f'USER INPUT: "{key_value}"')
        self.send_signal(self.signal_user_input, data={"key": key_value})
        return key_value

    def handle_signal_user_input(
        self, signal: str | None = None, data: dict[str, Any] | None = None
    ) -> None:
        self._log_handle_signal(signal=signal, data=data)

        if data is not None:
            if (user_key := data["key"]) is not None:
                if user_key in ["KEY_LEFT", "KEY_RIGHT", "KEY_DOWN", "KEY_UP"]:
                    player_movement = USER_MOVEMENT[user_key]
                    self.send_signal(
                        self.signal_player_movement, data={"direction": player_movement}
                    )

                elif data["key"] == "Q":
                    sys.exit(0)

        else:
            raise ValueError("Got empty data package.")


if __name__ == "__main__":
    term = blessed.Terminal()
    uinput = UserInput(term=term)
    uinput.wait_for_key()
