import textwrap
import json
import curses
from copy import deepcopy

from attrs import define, field

from glassdolls.utils import Loc
from glassdolls.state.signals import SignalSender
from glassdolls.state.maps import MapState

from glassdolls.constants import (
    HORIZ_PADDING,
    MAP_HEIGHT,
    MAP_WIDTH,
    MAX_SCREEN_WIDTH,
    TERMINAL_XY_INIT_MAP,
    VERT_PADDING,
    ASCII_CODES,
    DATA_GAME_DIALOGUE,
    DESCRIPTION_HEIGHT,
    USER_INPUT_OPTIONS,
)

PLAYER_COLOR = "CYAN"
DESC_TITLE_COLOR = "CYAN"
DESC_TEXT_COLOR = "WHITE"
OPTIONS_TITLE_COLOR = "CYAN"
OPTIONS_TEXT_COLOR = "WHITE"
LINE_COLOR = "YELLOW"
DUNGEON_WALL_COLOR = "WHITE"
INPUT_BORDER_COLOR = "CYAN"


@define
class Window:
    loc_start: Loc = field(default=Loc(1, 1))
    height: int = field(default=1)
    width: int = field(default=30)
    border: int = field(default=1)
    border_color: int = field(default=0)
    subwindow: "curses._CursesWindow" = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.subwindow = curses.newwin(
            self.height + (2 * self.border),
            self.width + (2 * self.border),
            self.loc_start.y,
            self.loc_start.x,
        )
        if self.border == 1:
            self.draw_border()

    def draw_border(self) -> None:
        height, width = self.subwindow.getmaxyx()

        for idx in range(0, width - 1):
            self.print_at(idx, 0, ASCII_CODES["Horizontal"], self.border_color)
            self.print_at(idx, height - 1, ASCII_CODES["Horizontal"], self.border_color)

        for jdx in range(0, height - 1):
            self.print_at(0, jdx, ASCII_CODES["Vertical"], self.border_color)
            self.print_at(width - 1, jdx, ASCII_CODES["Vertical"], self.border_color)

        self.print_at(0, 0, ASCII_CODES["UL_Corner"], self.border_color)
        self.print_at(width - 1, 0, ASCII_CODES["UR_Corner"], self.border_color)
        self.print_at(0, height - 1, ASCII_CODES["BL_Corner"], self.border_color)
        self.print_at(
            width - 1, height - 1, ASCII_CODES["BR_Corner"], self.border_color
        )

    def print_at(self, x: int, y: int, text: str, color: int = 0) -> None:
        # Color is the color pair number.

        # Why do we get an error here, and why do we ignore it?
        # SO: https://stackoverflow.com/a/41923640
        # Ref: https://docs.python.org/3/library/curses.html#curses.window.addstr
        try:
            self.subwindow.addstr(y, x, text, color)
        except curses.error:
            pass

    def refresh(self) -> None:
        self.subwindow.refresh()


@define
class InputWindow(Window):

    cursor: str | None = field(default=">")

    def __attrs_post_init__(self) -> None:
        Window.__attrs_post_init__(self)
        self.clear_window()

    def clear_window(self) -> None:
        self.subwindow.clear()  # Removes the border.
        self.subwindow.refresh()

    def create_user_input(self) -> str:
        self.draw_border()

        curses.echo()
        x_start = 1 if self.border else 0
        y_start = 1 if self.border else 0

        x_input_start = x_start + 1
        input_width = self.width - (2 * self.border)

        if self.cursor:
            self.subwindow.addch(y_start, x_start + 1, ">")
            x_input_start += 2
            input_width -= 2

        msg = self.subwindow.getstr(y_start, x_input_start, input_width).decode(
            encoding="utf-8"
        )
        self.clear_window()

        curses.noecho()
        return msg


@define
class MapDisplay(Window, SignalSender):
    _map_state: MapState = field(repr=False, default=MapState())
    player_loc: Loc = field(default=Loc(0, 0))
    map_color: int = field(default=0)
    player_color: int = field(default=512)

    def __attrs_post_init__(self) -> None:
        Window.__attrs_post_init__(self)
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

    def handle_player_loc_changed(
        self, signal: str | None = None, data: dict[str, Loc] | None = None
    ) -> None:
        self._log_handle_signal(signal=signal, data=data)
        if data is not None:
            if data.get("location") is not None:
                previous_loc = deepcopy(self.player_loc)
                self.player_loc = data["location"]
                self.map_state.update_visible(self.player_loc)
                # self.update_player_loc(previous_loc=previous_loc)
                self.display()
            else:
                raise ValueError(f"Got {data}, not a dict with key 'location'.")
        else:
            raise ValueError("Got empty data package.")


@define
class GameText:
    game_text_path: str = field(default=DATA_GAME_DIALOGUE)
    text: dict[str, str | list[str]] = field(repr=False, init=False)

    def __attrs_post_init__(self) -> None:
        with open(self.game_text_path, "r", encoding="utf-8") as f:
            self.text = json.load(f)

    def __getitem__(self, key: str) -> str | list[str]:
        return self.text[key]


@define
class DescriptionDisplay(Window, SignalSender):
    _title: str = field(default="")
    _text: str = field(default="")
    title_color: int = field(default=256)
    text_color: int = field(default=0)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value
        self.display()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value
        self.display()

    def clear(self) -> None:
        self.subwindow.clear()
        self.refresh()

    def display(self) -> None:
        self.subwindow.clear()
        if self.title != "":
            self.print_at(x=0, y=0, text=self.title, color=self.title_color)
            self.print_at(
                x=0,
                y=1,
                text="-" * len(self.title) + "\n\n",
                color=self.title_color,
            )

        if self.text != "":
            wrapped_text = textwrap.wrap(
                self.text,
                width=MAX_SCREEN_WIDTH - 5,
                initial_indent="",
                subsequent_indent="",
                expand_tabs=False,
                replace_whitespace=False,
                fix_sentence_endings=False,
                break_long_words=True,
                drop_whitespace=True,
                break_on_hyphens=True,
                tabsize=4,
                max_lines=None,
            )

            y_offset = 2 if self.title is not None else 0
            for jdx, line in enumerate(wrapped_text):
                self.print_at(
                    x=0,
                    y=jdx + y_offset,
                    text=line,
                    color=self.text_color,
                )
        self.refresh()

    def _wait_for_key(self) -> None:
        while True:
            val: str = self.subwindow.getkey()

            if val is not None:
                break

    def display_dialogue(self, text_list: list[str]) -> None:

        for line in text_list:
            self.text = line
            self._wait_for_key()
            curses.flushinp()
        self.clear()


@define
class GameScreen(SignalSender):
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
                jdx, _x, ASCII_CODES["Vertical"], self.color_map[LINE_COLOR]
            )

        # Horizontal
        _y = TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + VERT_PADDING
        for idx in range(HORIZ_PADDING, MAX_SCREEN_WIDTH + 1):
            self.term.addstr(
                _y, idx, ASCII_CODES["Horizontal"], self.color_map[LINE_COLOR]
            )

        # Crossings
        self.term.addstr(
            TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + VERT_PADDING,
            TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING,
            ASCII_CODES["ULR_Crossing"],
            self.color_map[LINE_COLOR],
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
                    _y, idx, ASCII_CODES["Horizontal"], self.color_map[LINE_COLOR]
                )
            except curses.error:
                pass

        self.term.refresh()
