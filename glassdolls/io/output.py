import textwrap
import json
import curses
from typing import Any
from copy import deepcopy

from attrs import define, field

from glassdolls.utils import Loc
from glassdolls.game.signals import SignalSender
from glassdolls.game.maps import Map

from blinker import NamedSignal, signal

from glassdolls import logger
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
)

USER_INPUT_OPTIONS = ["(←↑→↓) Move", "(L)ook", "(U)se", "(I)nventory"]


USER_COLOR = "hi_purple"
DESC_TITLE_COLOR = "cyan"
DESC_TEXT_COLOR = "white"
OPTIONS_TITLE_COLOR = "cyan"
OPTIONS_TEXT_COLOR = "white"
LINE_COLOR = "hi_red"
DUNGEON_WALL_COLOR = "white"


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

    def create_user_input(self) -> str:
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
        self.subwindow.clear()
        self.subwindow.refresh()

        curses.noecho()
        return msg


@define
class MapDisplay(Window, SignalSender):
    player_map_loc: Loc = field(init=False, default=Loc(0, 0))
    _current_map: Map = field(init=False, repr=False, default=Map())

    def __attrs_post_init__(self) -> None:
        Window.__attrs_post_init__(self)
        curses.curs_set(0)

    @property
    def current_map(self) -> Map:
        return self._current_map

    @current_map.setter
    def current_map(self, value: Map) -> None:
        self._current_map = value
        self.display()

    def display(self) -> None:
        self.subwindow.erase()

        if self.current_map is None:
            raise ValueError("Must initialize map in MapDisplay.")

        for jdx, row in enumerate(self.current_map.map_tiles):
            self.print_at(
                x=0,
                y=jdx,
                text="".join(row),
                color=0,
            )

        self.print_at(
            x=self.player_map_loc.x,
            y=self.player_map_loc.y,
            text="@",
            color=256,
        )
        self.refresh()

    def handle_player_loc_changed(
        self, signal: str | None = None, data: dict[str, Loc] | None = None
    ) -> None:
        self._log_handle_signal(signal=signal, data=data)
        if data is not None:
            if data.get("location") is not None:
                previous_loc = deepcopy(self.player_map_loc)
                self.player_map_loc = data["location"]
                # self.update_player_loc(previous_loc=previous_loc)
                self.display()
            else:
                raise ValueError(f"Got {data}, not a dict with key 'location'.")
        else:
            raise ValueError("Got empty data package.")


@define
class OptionsDisplay(Window, SignalSender):
    _options: list[str] = field(default=USER_INPUT_OPTIONS, repr=False)

    # Signals
    signal_options_updated: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        Window.__attrs_post_init__(self)

        self.signal_options_updated = signal(
            f"{self.__class__.__name__}_options_updated"
        )

    @property
    def options(self) -> list[str]:
        return self._options

    @options.setter
    def options(self, value: list[str]) -> None:
        self._options = value
        self.send_signal(self.signal_options_updated)

    def display(self) -> None:
        self.print_at(x=0, y=0, text="OPTIONS", color=265)
        self.print_at(x=0, y=1, text="=======", color=256)
        for jdx, option in enumerate(self.options):
            self.print_at(x=0, y=jdx + 2, text=option, color=0)
        self.refresh()


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
    _title: str | None = field(default=None)
    _text: str | None = field(default=None, repr=False)

    @property
    def title(self) -> str | None:
        return self._title

    @title.setter
    def title(self, value: str | None) -> None:
        self._title = value
        self.display()

    @property
    def text(self) -> str | None:
        return self._text

    @text.setter
    def text(self, value: str | None) -> None:
        self._text = value
        self.display()

    def display(self) -> None:
        self.subwindow.clear()
        self.refresh()
        if self.title is not None:
            self.print_at(x=0, y=0, text=self.title, color=0)
            self.print_at(
                x=0,
                y=1,
                text="-" * len(self.title) + "\n\n",
                color=0,
            )

        if self.text is not None:
            wrapped_text = textwrap.wrap(
                self.text,
                width=MAX_SCREEN_WIDTH - 5,
                initial_indent="",
                subsequent_indent="",
                expand_tabs=False,
                replace_whitespace=True,
                fix_sentence_endings=False,
                break_long_words=True,
                drop_whitespace=True,
                break_on_hyphens=True,
                tabsize=4,
                max_lines=None,
            )
            for text in wrapped_text:
                logger.debug(text)

            y_offset = 2 if self.title is not None else 0
            for jdx, line in enumerate(wrapped_text):
                logger.debug(f"on {jdx}, {line}...")
                self.print_at(
                    x=0,
                    y=jdx + y_offset,
                    text=line,
                    color=0,
                )
        self.refresh()


@define
class GameScreen(SignalSender):
    """Combines the Display elements into a full game screen."""

    term: "curses._CursesWindow" = field(repr=False)
    area_map: MapDisplay = field(init=False, repr=False)
    options: OptionsDisplay = field(init=False, repr=False)
    description: DescriptionDisplay = field(init=False, repr=False)
    input_window: InputWindow = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.area_map = MapDisplay(
            loc_start=TERMINAL_XY_INIT_MAP,
            height=MAP_HEIGHT,
            width=MAP_WIDTH,
            border=0,
            border_color=0,
        )

        self.options = OptionsDisplay(
            loc_start=TERMINAL_XY_INIT_MAP + Loc(MAP_WIDTH + (2 * HORIZ_PADDING), 0),
            height=MAP_HEIGHT + (2 * VERT_PADDING),
            width=20,
            border=0,
            border_color=0,
        )

        self.description = DescriptionDisplay(
            loc_start=TERMINAL_XY_INIT_MAP + Loc(0, MAP_WIDTH + (2 * VERT_PADDING)),
            height=DESCRIPTION_HEIGHT,
            width=MAX_SCREEN_WIDTH,
            border=0,
            border_color=0,
        )

        self.input_window = InputWindow(
            loc_start=Loc(
                TERMINAL_XY_INIT_MAP.x,
                TERMINAL_XY_INIT_MAP.y
                + MAP_HEIGHT
                + (2 * VERT_PADDING)
                + DESCRIPTION_HEIGHT
                + VERT_PADDING,
            ),
            height=1,
            width=MAX_SCREEN_WIDTH - 5,
            border=1,
            border_color=256,
        )

        self.options.refresh()
        self.draw_lines()
        self.input_window.refresh()

    def draw_lines(self) -> None:
        # Vertical
        _x = TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING
        for jdx in range(VERT_PADDING, TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + 1):
            self.term.addstr(jdx, _x, ASCII_CODES["Vertical"], 512)

        # Horizontal
        _y = TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + VERT_PADDING
        for idx in range(HORIZ_PADDING, MAX_SCREEN_WIDTH + 1):
            self.term.addstr(_y, idx, ASCII_CODES["Horizontal"], 512)

        # Crossings
        self.term.addstr(
            TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + VERT_PADDING,
            TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING,
            ASCII_CODES["ULR_Crossing"],
            512,
        )

        # Under Description, horizontal.
        _y = (
            TERMINAL_XY_INIT_MAP.y
            + MAP_HEIGHT
            + (2 * VERT_PADDING)
            + DESCRIPTION_HEIGHT
        )
        for idx in range(HORIZ_PADDING, MAX_SCREEN_WIDTH + 1):
            self.term.addstr(_y, idx, ASCII_CODES["Horizontal"], 512)

        self.term.refresh()
