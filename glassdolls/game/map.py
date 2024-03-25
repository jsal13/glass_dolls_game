# {
#     "dungeon": {
#         "unexplored": "░",
#         "puzzle": "∮",
#         "chest": "$",
#         "enemy": "ξ",
#         "person": "β",
#         "wall": "█",
#         "player": "@",
#         "stairs_down": "↘",
#         "stairs_up": "↗",
#         "nothing": " "
#     },
#     "cute_symbols_unused": [
#         "⌂"
#     ]
# }

import json

from attrs import define, field
from glassdolls.constants import MAPS_LEGEND_JSON, MAPS_DUNGEON_LEVEL_0_TXT

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

    def __init__(self, name: str, maps: dict[str, dict[str, list[str]]]) -> None:
        self.name = name
        self.maps = maps
        self._generate_fog_of_war_maps()

    def _generate_fog_of_war_maps(self) -> None:
        # TODO: Yuck.
        PLAYER_SYMBOL: str = MAPS_LEGEND["dungeon"]["player"]
        FOG_SYMBOL: str = MAPS_LEGEND["dungeon"]["unexplored"]
        for area in self.maps.keys():
            _area: list[str] = []
            # print(area, self.maps[area]["revealed"])
            for row in self.maps[area]["revealed"]:
                _row: list[str] = []
                for cell in row:
                    if cell != PLAYER_SYMBOL:
                        _row.append(FOG_SYMBOL)
                    else:
                        _row.append(PLAYER_SYMBOL)
                _area.append("".join(_row))
            self.maps[area]["player"] = _area

    def print_player_map(self, map_key: str) -> None:
        print("\n".join(self.maps[map_key]["player"]), sep="\n\n", end="\n\n")

    def print_revealed_map(self, map_key: str) -> None:
        print("\n".join(self.maps[map_key]["revealed"]), sep="\n\n", end="\n\n")


class Dungeon(Area):
    def __init__(self, name: str, maps: dict[str, dict[str, list[str]]]) -> None:
        super().__init__(name=name, maps=maps)


class Town(Area):
    def __init__(self, name: str, maps: dict[str, dict[str, list[str]]]) -> None:
        super().__init__(name=name, maps=maps)


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
                    row.strip() for row in maps_dungeon_level_0_txt.readlines()
                ]
            }
        },
    )
