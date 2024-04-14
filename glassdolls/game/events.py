from attrs import define, field

from glassdolls.utils import Loc
from glassdolls import logger
from glassdolls.io.utils import Color
from glassdolls.constants import FE_URI

@define 
class Event:
    # TODO: Should these have locs in them?
    loc: Loc
    etype: str = "General"
    symbol: str = field(default="∮")
    uri: str = field(default=FE_URI)
    color: Color = field(default="RED")
    active: bool = field(default=True)

    def __attrs_post_init__(self) -> None:
        pass
        

@define
class Events:
    data: list[Event]

    def _load_map(self) -> None:
        with open(self.map_file, "r", encoding="utf-8") as f:
            self.map_tiles = [list(i.strip()) for i in f.readlines()]

    def get_event_at(self, loc: Loc) -> Event:
        return self.data[loc]