from attrs import define, field

from glassdolls.utils import Loc
from glassdolls import logger
from glassdolls.constants import FE_URI


@define
class Event:
    # TODO: Should these have locs in them?
    loc: Loc = field(default=Loc(0, 0))
    etype: str = field(default="General")
    symbol: str = field(default="∮")
    uri: str = field(default=FE_URI)
    color: str = field(default="RED")
    active: bool = field(default=True)

    def __attrs_post_init__(self) -> None:
        pass


@define
class Events:
    data: dict[Loc, Event] = field(default={Loc(0, 0): Event()})

    def get_event_at(self, loc: Loc) -> Event:
        return self.data[loc]
