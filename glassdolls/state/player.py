from typing import Any

from attrs import define, field

from glassdolls.pubsub.producer import Producer
from glassdolls.utils import Loc
from glassdolls import logger


@define
class PlayerState:
    _loc: Loc = field(init=False)

    health: int = field(default=10)
    magic: int = field(default=0)
    strength: int = field(default=1)
    intelligence: int = field(default=1)

    producer: Producer = field(default=Producer(), repr=False)

    def __attrs_post_init__(self) -> None:
        self.loc = Loc(0, 0)  # Initialize Loc.
        self.producer.bind_queue(routing_key="player.loc_changed")
        self.producer.bind_queue(routing_key="player.look")

    @property
    def loc(self) -> Loc:
        return self._loc

    @loc.setter
    def loc(self, value: Loc) -> None:
        self._loc = value
        self.producer.send_to_queue(
            routing_key="player.loc_changed",
            body={"coords": self.loc.astuple()},
        )

    def handle_user_input_movement(self, dir: tuple[int, int]) -> None:
        self.loc += Loc.from_tuple(dir)

    def handle_user_input_look(self) -> None:
        self.producer.send_to_queue(
            routing_key="player.look", body={"coords": self.loc.astuple()}
        )
