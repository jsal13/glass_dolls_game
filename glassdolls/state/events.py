from enum import Enum, auto

from attrs import define, field
from cattrs.preconf.json import make_converter

from glassdolls import logger
from glassdolls.constants import FE_URI
from glassdolls.utils import Loc


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

    def make_title(self) -> str:
        return str(self.etype)

    def make_body(self) -> str:
        return f"{self.uri}/puzzle?code={self.code}"

    def as_json(self) -> str:
        """For use in JSON serialization."""
        return make_converter().dumps(self)


@define
class Events:
    data: dict[Loc, Event] = field(default={Loc(0, 0): Event()})

    def get_event_at(self, loc: Loc) -> Event:
        return self.data[loc]
