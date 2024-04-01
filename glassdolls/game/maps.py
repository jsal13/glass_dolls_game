from attrs import define, field

from glassdolls.constants import MAPS_DIR


@define
class Map:
    maps_dir: str = field(default=MAPS_DIR)
    map_title: str = field(default="dungeon_level_0.txt")
    map_tiles: list[list[str]] = field(repr=False, init=False)

    def __attrs_post_init__(self) -> None:
        self._load_map()

    def _load_map(self) -> None:
        with open(f"{self.maps_dir}/{self.map_title}", "r", encoding="utf-8") as f:
            self.map_tiles = [list(i) for i in f.readlines()]
