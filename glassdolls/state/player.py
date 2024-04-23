from typing import Any

from attrs import define, field
from blinker import NamedSignal, signal

from glassdolls.state.signals import SignalSender
from glassdolls.pubsub.producer import Producer
from glassdolls.utils import Loc
from glassdolls import logger


@define
class PlayerState(SignalSender):
    _loc: Loc = field(init=False)

    health: int = field(default=10)
    magic: int = field(default=0)
    strength: int = field(default=1)
    intelligence: int = field(default=1)

    producer: Producer = field(default=Producer(), repr=False)

    signal_player_look: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.producer.bind_queue(queue="player", routing_key="input")

        self.signal_player_look = signal(
            f"{self.__class__.__name__}_signal_player_look"
        )

        self.loc = Loc(0, 0)  # Initialize Loc.

    @property
    def loc(self) -> Loc:
        return self._loc

    @loc.setter
    def loc(self, value: Loc) -> None:
        self._loc = value
        self.producer.send_to_queue(
            routing_key="input",
            body={
                "event": "player_loc_changed",
                "data": {"location": self.loc.astuple()},
            },
        )

    def handle_signal_player_input_attempt_movement(
        self, signal: str | None = None, data: dict[str, Any] | None = None
    ) -> None:
        self._log_handle_signal(signal=signal, data=data)

        if data is not None:
            if data.get("direction") is not None:
                self.loc += data["direction"]
            else:
                raise ValueError(f"Got {data}, not a dict with key 'direction'.")
        else:
            raise ValueError("Got empty data package.")

    def handle_signal_player_input_attempt_look(
        self, signal: str | None = None, data: dict[str, Any] | None = None
    ) -> None:
        self._log_handle_signal(signal=signal, data=data)
        self.send_signal(self.signal_player_look, data={"location": self.loc})
