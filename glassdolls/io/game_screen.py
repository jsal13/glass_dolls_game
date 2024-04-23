import curses
from attrs import define, field

from glassdolls.constants import (
    ASCII_CODES,
    DESCRIPTION_HEIGHT,
    HORIZ_PADDING,
    MAP_HEIGHT,
    MAP_WIDTH,
    MAX_SCREEN_WIDTH,
    TERMINAL_XY_INIT_MAP,
    VERT_PADDING,
    COLORS,
)
from glassdolls import logger

from glassdolls.io.display_components.description_display_window import (
    DescriptionDisplay,
)
from glassdolls.io.display_components.input_window import InputWindow
from glassdolls.io.display_components.map_window import MapDisplay


@define
class GameScreen:
    """Combines the Display elements into a full game screen."""

    term: "curses._CursesWindow" = field(repr=False, default=curses.initscr())
    color_map: dict[str, int] = field(repr=False, default={})
    map_display: MapDisplay = field(repr=False, default=MapDisplay())
    options: DescriptionDisplay = field(repr=False, default=DescriptionDisplay())
    description: DescriptionDisplay = field(repr=False, default=DescriptionDisplay())
    input_window: InputWindow = field(repr=False, default=InputWindow())

    def draw_lines(self) -> None:
        # Vertical
        _x = TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING
        for jdx in range(VERT_PADDING, TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + 1):
            self.term.addstr(
                jdx, _x, ASCII_CODES["Vertical"], self.color_map[COLORS["line"]]
            )

        # Horizontal
        _y = TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + VERT_PADDING
        for idx in range(HORIZ_PADDING, MAX_SCREEN_WIDTH + 1):
            self.term.addstr(
                _y, idx, ASCII_CODES["Horizontal"], self.color_map[COLORS["line"]]
            )

        # Crossings
        self.term.addstr(
            TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + VERT_PADDING,
            TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING,
            ASCII_CODES["ULR_Crossing"],
            self.color_map[COLORS["line"]],
        )

        # Under Description, horizontal.
        _y = (
            TERMINAL_XY_INIT_MAP.y
            + MAP_HEIGHT
            + (2 * VERT_PADDING)
            + DESCRIPTION_HEIGHT
        )
        for idx in range(HORIZ_PADDING, MAX_SCREEN_WIDTH + 1):
            # This is a curses error when trying to draw in the lower-
            # right corner.  This is the solution.  Gross, I know.
            try:
                self.term.addstr(
                    _y, idx, ASCII_CODES["Horizontal"], self.color_map[COLORS["line"]]
                )
            except curses.error:
                pass

        self.term.refresh()
