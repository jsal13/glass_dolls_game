"""
Used for Player Input.
"""

from typing import Sequence
from attrs import define, field
from blessed.keyboard import Keystroke
import blessed
from blinker import NamedSignal

from glassdolls import logger
from glassdolls.signals import SignalSender


@define
class UserInput(SignalSender):
    term: "blessed.Terminal"

    # Signals
    signal_user_input: NamedSignal = field(init=False, repr=False)

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


if __name__ == "__main__":
    term = blessed.Terminal()
    uinput = UserInput(term=term)
    uinput.wait_for_key()
