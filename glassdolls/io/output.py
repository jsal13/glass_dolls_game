import curses
from typing import Any, Sequence
from copy import deepcopy

from attrs import define, field

from glassdolls import logger
from glassdolls.utils.game_utils import Loc
from glassdolls.constants import ASCII_CODES
from glassdolls.io.input import UserInput
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
    MAPS_DUNGEON_LEVEL_0_TXT,
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

    def display(
        self,
        x: int,
        y: int,
    ) -> None:
        self.print_at(x=x, y=y, text="OPTIONS", color=265)
        self.print_at(x=x, y=y + 1, text="=======", color=256)
        for jdx, option in enumerate(self.options):
            self.print_at(x=x, y=y + jdx + 2, text=option, color=0)

        for jdx in range((MAP_HEIGHT + VERT_PADDING) - len(self.options)):
            print()


# @define
# class LineDisplay(Window, SignalSender):

#     def vertical(self, x: int, y_min: int, y_max: int) -> None:
#         for jdx in range(y_min, y_max + 1):
#             self.print_at(x=x, y=jdx, text=ASCII_CODES["Vertical"], color=512)

#     def horizontal(self, y: int, x_min: int, x_max: int) -> None:
#         for idx in range(x_min, x_max + 1):
#             self.print_at(x=idx, y=y, text=ASCII_CODES["Horizontal"], color=512)

#     def crossing(self, x: int, y: int) -> None:
#         self.print_at(x=x, y=y, text=ASCII_CODES["ULR_Crossing"], color=512)


@define
class DescriptionDisplay(Window, SignalSender):
    _title: str | None = field(default=None)
    _text: str | None = field(default=None, repr=False)

    # Signals
    signal_title_updated: NamedSignal = field(init=False, repr=False)
    signal_text_updated: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.signal_title_updated = signal(f"{self.__class__.__name__}_title_updated")
        self.signal_text_updated = signal(f"{self.__class__.__name__}_text_updated")

    @property
    def title(self) -> str | None:
        return self._title

    @title.setter
    def title(self, value: str | None) -> None:
        self._title = value
        self.send_signal(self.signal_title_updated)

    @property
    def text(self) -> str | None:
        return self._text

    @text.setter
    def text(self, value: str | None) -> None:
        self._text = value
        self.send_signal(self.signal_text_updated)

    def display(self, x: int, y: int) -> None:
        if self.title is not None:
            self.print_at(x=x, y=y, text=self.title, color=0)
            self.print_at(
                x=x,
                y=y + 1,
                text="-" * len(self.title) + "\n\n",
                color=0,
            )

        # if self.text is not None:
        #     text_list = self.text.split("\n")
        #     y_offset = 2 if self.title is not None else 0
        #     for line in text_list:
        #         line_wrap_list = self.term.wrap(line, width=80)

        #         # If the line wraps, keep the text padded.
        #         line_wrap_list_indented = [
        #             (
        #                 (" " * (HORIZ_PADDING + 1)) + line_wrap_list[idx]
        #                 if idx > 0
        #                 else line_wrap_list[idx]
        #             )
        #             for idx in range(len(line_wrap_list))
        #         ]

        #         self.print_at(
        #             x=x,
        #             y=y + y_offset,
        #             text="\n".join(line_wrap_list_indented) + "\n\n",
        #             color=DESC_TEXT_COLOR,
        #         )

        #         y_offset += len(line_wrap_list) + 2


@define
class GameScreen(SignalSender):
    """Combines the Display elements into a full game screen."""

    term: "curses._CursesWindow" = field(repr=False)
    area_map: MapDisplay = field(init=False, repr=False)
    # options: OptionsDisplay = field(init=False, repr=False)
    # description: DescriptionDisplay = field(init=False, repr=False)
    # Signals.
    signal_user_input: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        # Initialize the stuff.
        self.area_map = MapDisplay(
            loc_start=TERMINAL_XY_INIT_MAP,
            height=MAP_HEIGHT,
            width=MAP_WIDTH,
            border=0,
            border_color=0,
        )

        # self.options = OptionsDisplay(term=self.term)
        self.draw_lines()
        # self.description = DescriptionDisplay(term=self.term)

        self.signal_user_input = signal(f"{self.__class__.__name__}_user_input")

        # Subscribe to Signals.
        # self.description.signal_title_updated.connect(self.handle_display_updates)
        # self.description.signal_text_updated.connect(self.handle_display_updates)

    def draw_lines(self) -> None:
        self.term.vline(
            VERT_PADDING,
            TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING,
            "|",
            TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT,
        )

        self.term.hline(
            TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + VERT_PADDING,
            HORIZ_PADDING,
            "-",
            MAX_SCREEN_WIDTH,
        )

        self.term.addch(
            TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + VERT_PADDING,
            TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING,
            "+",
        )

    # def _refresh_screen(self) -> None:
    #     print(f"{self.term.home}{self.term.clear}")

    # def refresh_display(self) -> None:
    #     self.area_map.display()

    #     self.options.display(
    #         x=(TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING + 1 + HORIZ_PADDING),
    #         y=TERMINAL_XY_INIT_MAP.y,
    #     )
    #     self.description.display(
    #         x=TERMINAL_XY_INIT_MAP.x,
    #         y=TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + (2 * VERT_PADDING + 1),
    #     )

    # def handle_display_updates(
    #     self, signal: str | None = None, data: dict[str, Any] | None = None
    # ) -> None:
    #     self._log_handle_signal(signal=signal, data=data)
    #     self.refresh_display()
