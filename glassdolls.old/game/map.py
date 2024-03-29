import json
from enum import Enum, auto

from attrs import define, field
from glassdolls.constants import MAPS_LEGEND_JSON, MAPS_DUNGEON_LEVEL_0_TXT
from glassdolls.game.utils import Loc


class Result(Enum):
    SUCCESS = auto()
    WALL = auto()
    PERSON = auto()
    TREASURE = auto()
    PUZZLE = auto()
    STAIRS = auto()


DIR_MAP = {"w": Loc(0, -1), "e": Loc(0, 1), "n": Loc(1, 0), "s": Loc(0, 1)}

with (open(MAPS_LEGEND_JSON, "r", encoding="utf-8") as maps_legend_json,):
    MAPS_LEGEND = json.load(maps_legend_json)

# What does a map look like?
# {
#     "level_number": {
#         "revealed": ["xxx", "xxx", "xxx"],
#         "player": {"yyy", "yyy", "yyy"},
#     }
# }


class Area:

    def __init__(self, name: str, maps: dict[str, dict[str, list[list[str]]]]) -> None:
        self.name = name
        self.maps = maps
        self._generate_fog_of_war_maps()

    def place_player(
        self,
        level: str,
        loc: Loc,
    ) -> None: ...

    def _generate_fog_of_war_maps(self) -> None:
        # TODO: Yuck.
        PLAYER_SYMBOL: str = MAPS_LEGEND["dungeon"]["player"]
        FOG_SYMBOL: str = MAPS_LEGEND["dungeon"]["unexplored"]
        for area in self.maps.keys():
            _area: list[list[str]] = []
            # print(area, self.maps[area]["revealed"])
            for row in self.maps[area]["revealed"]:
                _row: list[str] = []
                for cell in row:
                    if cell != PLAYER_SYMBOL:
                        _row.append(FOG_SYMBOL)
                    else:
                        _row.append(PLAYER_SYMBOL)
                _area.append(_row)
            self.maps[area]["player"] = _area

    def get_printable_player_map(self, map_key: str) -> str:
        _m = self.maps[map_key]["player"]
        return "\n".join("".join(row) for row in self.maps[map_key]["player"])

    def get_printable_revealed_map(self, map_key: str) -> str:
        return "\n".join("".join(row) for row in self.maps[map_key]["revealed"])


class Dungeon(Area):
    def place_player(
        self,
        level: str,
        loc: Loc,
    ) -> None:
        revealed_value = self.maps[level]["revealed"][loc.y][loc.x]
        self.maps[level]["player"][loc.y][loc.x] = revealed_value
        self.maps[level]["revealed"][loc.y][loc.x] = "@"


class Town(Area):
    pass


@define
class GameAreas:
    dungeons: dict[str, Dungeon] = field(default={})
    towns: dict[str, Town] = field(default={})


GAME_AREAS = GameAreas()

with (
    open(MAPS_DUNGEON_LEVEL_0_TXT, "r", encoding="utf-8") as maps_dungeon_level_0_txt,
):

    GAME_AREAS.dungeons["Start"] = Dungeon(
        name="Start",
        maps={
            "0": {
                "revealed": [
                    list(row.strip()) for row in maps_dungeon_level_0_txt.readlines()
                ]
            }
        },
    )
