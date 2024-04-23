import curses
import sys
from typing import Any

from attrs import define, field

from glassdolls import logger
from glassdolls.constants import USER_MOVEMENT
from glassdolls.pubsub.producer import Producer


@define
class UserInput:
    subwindow: "curses._CursesWindow"
    producer: Producer

    @classmethod
    def create_user_input(cls) -> "UserInput":
        producer = Producer.create_standard_producer()
        subwindow = curses.newwin(1, 1, 0, 0)
        _cls = cls(subwindow=subwindow, producer=producer)

        # REF: https://docs.python.org/3/library/curses.html#curses.window.keypad
        _cls.subwindow.keypad(True)

        _cls.producer.bind_queue(routing_key="user_input.attempt_move")
        _cls.producer.bind_queue(routing_key="user_input.look")

        return _cls

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
            self.producer.send_to_queue(routing_key="user_input.look", body=body)

        elif upper_key_value == "Q":
            sys.exit(0)
