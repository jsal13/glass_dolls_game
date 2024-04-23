import curses
from typing import Any
import sys

from attrs import define, field

from glassdolls import logger
from glassdolls.constants import USER_MOVEMENT
from glassdolls.pubsub.producer import Producer


@define
class UserInput:
    subwindow: "curses._CursesWindow" = field(init=False, repr=False)
    producer: Producer = field(default=Producer(), repr=False)

    def __attrs_post_init__(self) -> None:
        self.subwindow = curses.newwin(
            1,
            1,
            0,
            0,
        )
        # REF: https://docs.python.org/3/library/curses.html#curses.window.keypad
        self.subwindow.keypad(True)

        self.producer.bind_queue(routing_key="user_input.attempt_move")
        self.producer.bind_queue(routing_key="user_input.look")

    def wait_for_key(self) -> str:
        while True:
            val: str = self.subwindow.getkey()

            if val is not None:
                break

        self.triage_user_input(key_value=val)
        return val

    def triage_user_input(self, key_value: str) -> None:
        upper_key_value = key_value.upper()
        body: dict[str, Any] = {"key_value": upper_key_value}

        if upper_key_value in USER_MOVEMENT:
            loc = USER_MOVEMENT[key_value]
            body["direction"] = loc.astuple()
            self.producer.send_to_queue(
                routing_key="user_input.attempt_move",
                body=body,
            )

        elif upper_key_value == "L":  # Look
            logger.debug(f"User input 'Look'.")
            self.producer.send_to_queue(routing_key="user_input.look", body=body)

        elif upper_key_value == "Q":
            sys.exit(0)
