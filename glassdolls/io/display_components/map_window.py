import curses
from copy import deepcopy

from attrs import define, field

from glassdolls.io.display_components.window import Window
from glassdolls.state.map import MapState
from glassdolls.utils import Loc


@define
class MapDisplay(Window):
    _map_state: MapState = field(repr=False, default=MapState())
    player_loc: Loc = field(default=Loc(0, 0))
    map_color: int = field(default=0)
    player_color: int = field(default=512)

    def __attrs_post_init__(self) -> None:
        self.init_window()
        curses.curs_set(0)

    @property
    def map_state(self) -> MapState:
        return self._map_state

    @map_state.setter
    def map_state(self, value: MapState) -> None:
        self._map_state = value
        self.display()

    def display(self) -> None:
        self.subwindow.erase()

        if self.map_state is None:
            raise ValueError("Must initialize map in MapDisplay.")

        # Print map.
        for jdx, row in enumerate(self.map_state.visible_map_tiles):
            self.print_at(
                x=0,
                y=jdx,
                text="".join(row),
                color=self.map_color,
            )

        # Print event symbols.
        for loc in self.map_state.events.data.items():
            self.print_at(x=loc[0].x, y=loc[0].y, text=loc[1].symbol, color=128 * 5)

        # Print Player loc.
        # Always print player last so nothing overlaps it.
        self.print_at(
            x=self.player_loc.x,
            y=self.player_loc.y,
            text="@",
            color=self.player_color,
        )

        self.refresh()

    def handle_player_loc_changed(self, coords: tuple[int, int]) -> None:
        previous_loc = deepcopy(self.player_loc)
        self.player_loc = Loc.from_tuple(coords=coords)
        self.map_state.update_visible(self.player_loc)
        self.display()
