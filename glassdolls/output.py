from typing import Sequence, Any

from attrs import define, field
from blinker import signal, NamedSignal
from blessed import Terminal
from blessed.keyboard import Keystroke

from glassdolls import logger
from glassdolls.signals import SignalSender
from glassdolls.utils import Loc
from glassdolls.constants import (
    HORIZ_PADDING,
    VERT_PADDING,
    MAX_SCREEN_WIDTH,
    MAP_HEIGHT,
    MAP_WIDTH,
    TERMINAL_XY_INIT_MAP,
    ASCII_CODES,
)

USER_INPUT_OPTIONS = ["(←↑→↓) Move", "(L)ook", "(U)se", "(I)nventory"]


@define
class TerminalPrinter:
    term: Terminal

    def print_at(self, x: int, y: int, text: str, color: str = "white") -> None:
        color_text: str

        if color == "white":
            color_text = self.term.white(text)
        elif color == "black":
            color_text = self.term.black(text)
        elif color == "red":
            color_text = self.term.red(text)
        elif color == "green":
            color_text = self.term.green(text)
        elif color == "yellow":
            color_text = self.term.yellow(text)
        elif color == "blue":
            color_text = self.term.blue(text)
        elif color == "magenta":
            color_text = self.term.magenta(text)
        elif color == "cyan":
            color_text = self.term.cyan(text)
        elif color == "yellow":
            color_text = self.term.yellow(text)
        # Below NOT supported on 8-bit consoles.
        elif color == "pink":
            color_text = self.term.pink(text)
        else:
            raise ValueError(f"No such color {color} implemented.")

        print(self.term.move_xy(x=x, y=y) + color_text, end="")


@define
class MapDisplay(TerminalPrinter, SignalSender):
    term: Terminal
    map_ascii: list[list[str]] = field(repr=False)
    player_map_loc: Loc = field(default=Loc(2, 2))
    x_start: int = field(default=TERMINAL_XY_INIT_MAP.x, repr=False)
    y_start: int = field(default=TERMINAL_XY_INIT_MAP.y, repr=False)

    # Signals
    signal_player_map_loc_updated: NamedSignal = field(init=False, repr=False)

    def display(self) -> None:
        for jdx, row in enumerate(self.map_ascii):
            self.print_at(x=self.x_start, y=self.y_start + jdx, text="".join(row))

        self.display_user(x=self.player_map_loc.x, y=self.player_map_loc.y)
        print()

    def display_user(self, x: int, y: int) -> None:
        self.print_at(x=self.x_start + x, y=self.y_start + y, text="@", color="green")


@define
class OptionsDisplay(TerminalPrinter, SignalSender):
    term: Terminal
    _options: list[str] = field(default=USER_INPUT_OPTIONS, repr=False)

    # Signals
    signal_options_updated: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
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
        self.print_at(x=x, y=y, text="OPTIONS")
        self.print_at(x=x, y=y + 1, text="=======")
        for jdx, option in enumerate(self.options):
            self.print_at(x=x, y=y + jdx + 2, text=option)

        for jdx in range((MAP_HEIGHT + VERT_PADDING) - len(self.options)):
            print()


@define
class DescriptionDisplay(TerminalPrinter, SignalSender):
    term: Terminal
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
            self.print_at(x=x, y=y, text=self.title, color="cyan")
            self.print_at(
                x=x, y=y + 1, text="-" * len(self.title) + "\n\n", color="cyan"
            )

        if self.text is not None:
            text_list = self.text.split("\n")
            y_offset = 2 if self.title is not None else 0
            for line in text_list:
                line_wrap_list = self.term.wrap(line, width=80)

                # If the line wraps, keep the text padded.
                line_wrap_list_indented = [
                    (
                        (" " * (HORIZ_PADDING + 1)) + line_wrap_list[idx]
                        if idx > 0
                        else line_wrap_list[idx]
                    )
                    for idx in range(len(line_wrap_list))
                ]

                self.print_at(
                    x=x,
                    y=y + y_offset,
                    text="\n".join(line_wrap_list_indented) + "\n\n",
                )

                y_offset += len(line_wrap_list) + 2


@define
class LineDisplay(TerminalPrinter, SignalSender):

    def vertical(self, x: int, y_min: int, y_max: int) -> None:
        for jdx in range(y_min, y_max + 1):
            self.print_at(x=x, y=jdx, text=ASCII_CODES["Vertical"], color="pink")

    def horizontal(self, y: int, x_min: int, x_max: int) -> None:
        for idx in range(x_min, x_max + 1):
            self.print_at(x=idx, y=y, text=ASCII_CODES["Horizontal"], color="pink")

    def crossing(self, x: int, y: int) -> None:
        self.print_at(
            x=x, y=y, text=ASCII_CODES["Up_Left_Right_Crossing"], color="pink"
        )


@define
class GameScreen(SignalSender):
    """Combines the Display elements into a full game screen."""

    term: Terminal = field(repr=False)
    area_map: MapDisplay = field(init=False, repr=False)
    options: OptionsDisplay = field(init=False, repr=False)
    line: LineDisplay = field(init=False, repr=False)
    description: DescriptionDisplay = field(init=False, repr=False)
    # Signals.
    signal_user_input: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        # Initialize the stuff.
        self.area_map = MapDisplay(
            term=self.term, map_ascii=[["." for _ in range(16)] for _ in range(16)]
        )
        self.options = OptionsDisplay(term=self.term)
        self.line = LineDisplay(term=self.term)
        self.description = DescriptionDisplay(term=self.term)

        self.signal_user_input = signal(f"{self.__class__.__name__}_user_input")

        # Subscribe to Signals.
        self.description.signal_title_updated.connect(self.handle_display_updates)
        self.description.signal_text_updated.connect(self.handle_display_updates)

    def _refresh_screen(self) -> None:
        print(f"{self.term.home}{self.term.clear}")

    def refresh_display(self) -> None:
        self._refresh_screen()
        self.line.vertical(
            x=TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING,
            y_min=VERT_PADDING,
            y_max=TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + VERT_PADDING,
        )
        self.line.horizontal(
            y=TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + VERT_PADDING,
            x_min=HORIZ_PADDING,
            x_max=MAX_SCREEN_WIDTH - HORIZ_PADDING,
        )
        self.line.crossing(
            x=TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING,
            y=TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + VERT_PADDING,
        )
        self.area_map.display()

        self.options.display(
            x=(TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING + 1 + HORIZ_PADDING),
            y=TERMINAL_XY_INIT_MAP.y,
        )
        self.description.display(
            x=TERMINAL_XY_INIT_MAP.x,
            y=TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + (2 * VERT_PADDING + 1),
        )

    def handle_player_loc_changed(
        self, signal: str | None = None, data: dict[str, Loc] | None = None
    ) -> None:
        # Just update the display.
        self._log_handle_signal(signal=signal, data=data)

        if data is not None:
            if data["location"] is not None:
                self.area_map.player_map_loc = data["location"]
                self.refresh_display()

    def handle_display_updates(
        self, signal: str | None = None, data: dict[str, Any] | None = None
    ) -> None:
        self._log_handle_signal(signal=signal, data=data)
        self.refresh_display()
