from attrs import define, field

from glassdolls.constants import MAP_DIR, MAP_LEGEND_JSON
from glassdolls.utils import Loc
from glassdolls import logger
from glassdolls._types import MapTiles


@define
class Map:
    map_dir: str = field(default=MAP_DIR)
    map_title: str = field(default="dungeon_level_0.txt")
    map_tiles: MapTiles = field(repr=False, init=False)

    def __attrs_post_init__(self) -> None:
        self._load_map()

    def _load_map(self) -> None:
        with open(f"{self.map_dir}/{self.map_title}", "r", encoding="utf-8") as f:
            self.map_tiles = [list(i) for i in f.readlines()]

    def _is_collider(self, loc: Loc) -> bool:
        if self.map_tiles[loc.y][loc.x] == MAP_LEGEND_JSON["dungeon"]["wall"]:
            logger.debug(f"Player hit collider @ {loc}.")
            return True
        return False
