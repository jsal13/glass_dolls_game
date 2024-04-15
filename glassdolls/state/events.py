from enum import Enum, auto
from attrs import define, field

from glassdolls.utils import Loc
from glassdolls import logger
from glassdolls.constants import FE_URI


class EventType(Enum):
    puzzle = auto()
    person = auto()


@define
class Event:
    etype: EventType = field(default=EventType.puzzle)
    symbol: str = field(default="∮")
    uri: str = field(default=FE_URI)
    color: str = field(default="RED")
    active: bool = field(default=True)
    text: str = field(default=f"This is a test Event.")

    def __attrs_post_init__(self) -> None:
        pass


@define
class Events:
    data: dict[Loc, Event] = field(default={Loc(0, 0): Event()})

    def get_event_at(self, loc: Loc) -> Event:
        return self.data[loc]
