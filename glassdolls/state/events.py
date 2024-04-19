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
    code: str = field(default="")
    color: str = field(default="RED")
    active: bool = field(default=True)

    def __attrs_post_init__(self) -> None:
        pass

    def make_title(self) -> str:
        return str(self.etype)

    def make_body(self) -> str:
        return f"{self.uri}/puzzle?code={self.code}"


@define
class Events:
    data: dict[Loc, Event] = field(default={Loc(0, 0): Event()})

    def get_event_at(self, loc: Loc) -> Event:
        return self.data[loc]
