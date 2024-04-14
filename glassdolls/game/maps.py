from attrs import define, field

from glassdolls.constants import MAP_LEGEND_JSON, MAP_TOWN_TEST_FILE
from glassdolls.utils import Loc
from glassdolls import logger
from glassdolls._types import MapTiles
from glassdolls.game.events import Events


@define
class MapState:
    events: Events = field(repr=False)
    map_file: str = field(default=MAP_TOWN_TEST_FILE)
    map_tiles: MapTiles = field(repr=False, init=False)
    visible_map_tiles: MapTiles = field(repr=False, init=False)
    # num_visible_tiles_vert: int = field(default=MAP_HEIGHT)
    # num_visible_tiles_horiz: int = field(default=MAP_WIDTH)

    def __attrs_post_init__(self) -> None:
        self._load_map()
        self.update_visible(player_loc=Loc(1,1))

    def _load_map(self) -> None:
        with open(self.map_file, "r", encoding="utf-8") as f:
            self.map_tiles = [list(i.strip()) for i in f.readlines()]

    def is_collider(self, loc: Loc) -> bool:
        if self.map_tiles[loc.y][loc.x] == MAP_LEGEND_JSON["dungeon"]["wall"]:
            logger.debug(f"Player hit collider @ {loc}.")
            return True
        return False
    
    def is_event(self, loc: Loc) -> bool:
        if self.events.data.get(loc) is not None:
            logger.debug(f"Player is on an event @ {loc}.")
            return True
        return False
    
    def update_visible(self, player_loc: Loc) -> None:
        # TODO: This should be put in.
        self.visible_map_tiles = self.map_tiles
        # _visible_tiles = np.array(self.map_tiles)

        # left_right_tiles = int((self.num_visible_tiles_horiz - 1) / 2)
        # up_down_tiles = int((self.num_visible_tiles_horiz - 1) / 2)



        # tiles_left = max(0, player_loc.x - left_right_tiles)
        # tiles_up =  max(0, player_loc.y - up_down_tiles)
        # tiles_right = len(self.map_tiles[0]) - self.num_visible_tiles_horiz + left_right_tiles
        # tiles_down = len(self.map_tiles) - self.num_visible_tiles_vert + up_down_tiles
        
        # self.visible_map_tiles = _visible_tiles[tiles_up:tiles_down, tiles_left:tiles_right].tolist()  # Right-hand is inclusive.
        # logger.debug("Updating visible map...")
        # logger.debug(f"Map now has boundaries: {tiles_left}, {tiles_right}, {tiles_up}, {tiles_down}.")
