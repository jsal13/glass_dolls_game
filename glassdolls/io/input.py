import sys
import curses
from attrs import define, field

from blinker import signal, NamedSignal

from glassdolls import logger
from glassdolls.constants import USER_MOVEMENT
from glassdolls.game.signals import SignalSender


@define
class UserInput(SignalSender):
    subwindow: "curses._CursesWindow" = field(init=False, repr=False)

    # Signals
    signal_user_input: NamedSignal = field(init=False, repr=False)
    signal_player_input_movement: NamedSignal = field(init=False, repr=False)
    signal_key_pressed: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.subwindow = curses.newwin(
            1,
            1,
            0,
            0,
        )
        # REF: https://docs.python.org/3/library/curses.html#curses.window.keypad
        self.subwindow.keypad(True)

        self.signal_user_input = signal(f"{self.__class__.__name__}_user_input")
        self.signal_player_input_movement = signal(
            f"{self.__class__.__name__}_player_input_movement"
        )

    def wait_for_key(self) -> str:
        while True:
            val: str = self.subwindow.getkey()

            if val is not None:
                break

        logger.debug(f"USER INPUT: {val}")
        self.triage_user_input(key_value=val)
        return val

    def triage_user_input(self, key_value: str) -> None:
        upper_key_value = key_value.upper()

        if upper_key_value in USER_MOVEMENT:
            player_movement = USER_MOVEMENT[key_value]
            self.send_signal(
                self.signal_player_input_movement, data={"direction": player_movement}
            )
        elif upper_key_value == "Q":
            sys.exit(0)
