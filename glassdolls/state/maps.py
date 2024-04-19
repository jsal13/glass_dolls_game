from typing import Any

from attrs import define, field
from blinker import NamedSignal, signal

from glassdolls import logger
from glassdolls._types import MapTiles
from glassdolls.constants import MAP_LEGEND_JSON, MAP_TOWN_TEST_FILE
from glassdolls.state.events import Events
from glassdolls.state.signals import SignalSender
from glassdolls.utils import Loc


@define
class MapState(SignalSender):
    events: Events = field(repr=False, default=Events())
    map_file: str = field(default=MAP_TOWN_TEST_FILE)
    map_tiles: MapTiles = field(repr=False, init=False)
    visible_map_tiles: MapTiles = field(repr=False, init=False)
    # num_visible_tiles_vert: int = field(default=MAP_HEIGHT)
    # num_visible_tiles_horiz: int = field(default=MAP_WIDTH)

    signal_player_looked_at_event: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self._load_map()
        self.visible_map_tiles = self.map_tiles  # TODO: Temp fix before update_visible.
        # self.update_visible(player_loc=Loc(1,1))

        self.signal_player_looked_at_event = signal(
            f"{self.__class__.__name__}_player_looked_at_event"
        )

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

    def handle_signal_player_look(
        self, signal: str | None = None, data: dict[str, Any] | None = None
    ) -> None:
        self._log_handle_signal(signal=signal, data=data)

        if data is not None:
            if data.get("location") is not None:
                event_exists = self.is_event(loc=data["location"])
                if event_exists:
                    self.send_signal(
                        self.signal_player_looked_at_event,
                        data={"event": self.events.data[data["location"]]},
                    )
                else:
                    logger.debug("Nothing looks interesting...")

            else:
                raise ValueError(f"Got {data}, not a dict with key 'location'.")
        else:
            raise ValueError("Got empty data package.")
