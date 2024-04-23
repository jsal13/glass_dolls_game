from typing import Any

from attrs import define, field

from glassdolls import logger
from glassdolls.pubsub.producer import Producer
from glassdolls.utils import Loc


@define
class PlayerState:
    _loc: Loc

    health: int = field(default=10)
    magic: int = field(default=0)
    strength: int = field(default=1)
    intelligence: int = field(default=1)

    producer: Producer = field(default=Producer.create_standard_producer(), repr=False)

    @classmethod
    def create_default_playerstate(
        cls, health: int = 10, magic: int = 0, strength: int = 1, intelligence: int = 1
    ) -> "PlayerState":
        producer = Producer.create_standard_producer()

        _cls = cls(
            loc=Loc(0, 0),  # Is this how we do a property?
            health=health,
            magic=magic,
            strength=strength,
            intelligence=intelligence,
            producer=producer,
        )

        # Binding queues.
        _cls.producer.bind_queue(routing_key="player.loc_changed")
        _cls.producer.bind_queue(routing_key="player.look")

        return _cls

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
