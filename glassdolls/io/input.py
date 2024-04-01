import sys
import curses
from attrs import define, field

from blinker import signal, NamedSignal

from glassdolls import logger
from glassdolls.constants import USER_MOVEMENT
from glassdolls.game.signals import SignalSender


@define
class UserInput(SignalSender):
    term: "curses._CursesWindow"

    # Signals
    signal_user_input: NamedSignal = field(init=False, repr=False)
    signal_player_movement: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.signal_user_input = signal(f"{self.__class__.__name__}_user_input")
        self.signal_player_movement = signal(f"{self.__class__.__name__}_user_movement")

    def wait_for_key(self) -> None:
        while True:
            val: str = self.term.getkey()

            if val is not None:
                break

        logger.debug(f"USER INPUT: {val}")
        self.triage_user_input(key_value=val)

    def triage_user_input(self, key_value: str) -> None:
        upper_key_value = key_value.upper()
        if upper_key_value in ["KEY_LEFT", "KEY_RIGHT", "KEY_DOWN", "KEY_UP"]:
            player_movement = USER_MOVEMENT[key_value]
            self.send_signal(
                self.signal_player_movement, data={"direction": player_movement}
            )
        elif upper_key_value == "Q":
            sys.exit(0)
