from typing import Sequence, Any

from attrs import define, field
from blinker import signal, NamedSignal
from blessed import Terminal
from blessed.keyboard import Keystroke

from glassdolls import logger
from glassdolls.utils import Loc, send_signal
from glassdolls.constants import MAPS_DUNGEON_LEVEL_0_TXT, DATA_GAME_DIALOGUE

HORIZ_PADDING = 2
VERT_PADDING = 1
USER_INPUT_OPTIONS = ["(←↑→↓) Move", "(L)ook", "(U)se", "(I)nventory"]
MAX_SCREEN_WIDTH = 80
MAP_WIDTH = 16
MAP_HEIGHT = 16
TERMINAL_XY_INIT_MAP = Loc(1 + HORIZ_PADDING, 1 + VERT_PADDING)  # Upper-left.
ASCII_CODES = {
    "Vertical": "║",
    "Horizontal": "═",
    "Crossing": "╬",
    "Up_Left_Right_Crossing": "╩",
}

USER_MOVEMENT = {
    "KEY_LEFT": Loc(-1, 0),
    "KEY_RIGHT": Loc(1, 0),
    "KEY_DOWN": Loc(0, 1),
    "KEY_UP": Loc(0, -1),
}


@define
class Display:
    term: Terminal

    def print_at(self, x: int, y: int, text: str, color: str = "white") -> None:
        color_text: str

        if color == "white":
            color_text = self.term.white(text)
        elif color == "cyan":
            color_text = self.term.cyan(text)
        elif color == "pink":
            color_text = self.term.pink(text)
        elif color == "green":
            color_text = self.term.green(text)
        else:
            raise ValueError(f"No such color {color} implemented.")

        print(self.term.move_xy(x=x, y=y) + color_text, end="")


@define
class MapDisplay(Display):
    term: Terminal
    map_ascii: list[list[str]] = field(repr=False)
    _player_loc: Loc = field(default=Loc(2, 2))
    x_start: int = field(default=TERMINAL_XY_INIT_MAP.x, repr=False)
    y_start: int = field(default=TERMINAL_XY_INIT_MAP.y, repr=False)

    # Signals
    signal_player_loc_updated: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.signal_player_loc_updated = signal(
            f"{self.__class__.__name__}_player_loc_updated"
        )

    @property
    def player_loc(self) -> Loc:
        return self._player_loc

    @player_loc.setter
    def player_loc(self, value: Loc) -> None:
        self._player_loc = value
        send_signal(self.signal_player_loc_updated, data={"loc": self.player_loc})

    def display(self) -> None:
        for jdx, row in enumerate(self.map_ascii):
            self.print_at(x=self.x_start, y=self.y_start + jdx, text="".join(row))

        self.display_user(x=self.player_loc.x, y=self.player_loc.y)
        print()

    def display_user(self, x: int, y: int) -> None:
        self.print_at(x=self.x_start + x, y=self.y_start + y, text="@", color="green")

    def handle_signal_user_input(
        self, sender: NamedSignal | None = None, data: dict[str, Any] | None = None
    ) -> None:
        if sender is not None:
            logger.debug(
                f"{self.__class__.__name__} received signal: {sender} with data: {data}"
            )

        if data is not None:
            if data["key"] is not None:
                player_movement = USER_MOVEMENT[data["key"]]
        else:
            raise ValueError("Got empty data package.")

        self.player_loc += player_movement


@define
class OptionsDisplay(Display):
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
        send_signal(self.signal_options_updated)

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
class DescriptionDisplay(Display):
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
        send_signal(self.signal_title_updated)

    @property
    def text(self) -> str | None:
        return self._text

    @text.setter
    def text(self, value: str | None) -> None:
        self._text = value
        send_signal(self.signal_text_updated)

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
class LineDisplay(Display):

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
class UI:
    term: Terminal = field(repr=False)
    area_map: MapDisplay = field(repr=False)
    options: OptionsDisplay = field(repr=False)
    line: LineDisplay = field(repr=False)
    description: DescriptionDisplay = field(repr=False)

    # Signals.
    signal_user_input: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.signal_user_input = signal(f"{self.__class__.__name__}_user_input")

        # Connect Signals.
        self.signal_user_input.connect(self.area_map.handle_signal_user_input)

        # Subscribe to Signals.
        self.description.signal_title_updated.connect(self.handle_display_updates)
        self.description.signal_text_updated.connect(self.handle_display_updates)
        self.area_map.signal_player_loc_updated.connect(self.handle_display_updates)

    def wait_for_key(self, user_key: str | None = None) -> Keystroke:
        """
        Wait for user_input with value ``key``.

        Notes
        -----
        See: https://blessed.readthedocs.io/en/latest/keyboard.html#keycodes

        Args:
            user_key (str | None, optional): Keycode for desired user key.  None will take any key. Defaults to None.
        """
        with self.term.cbreak():
            while True:
                val = self.term.inkey()
                if val.is_sequence and ((user_key is None) or (val.name == user_key)):
                    send_signal(self.signal_user_input, data={"key": val.name})
                    break
        return val

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
            y=VERT_PADDING,
        )
        self.description.display(
            x=TERMINAL_XY_INIT_MAP.x,
            y=TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + (2 * VERT_PADDING + 1),
        )

    def handle_display_updates(
        self, sender: NamedSignal | None = None, data: dict[str, Any] | None = None
    ) -> None:
        if sender is not None:
            logger.debug(
                f"{self.__class__.__name__} received signal: {sender} with data: {data}"
            )
        self.refresh_display()


if __name__ == "__main__":
    with open(MAPS_DUNGEON_LEVEL_0_TXT, "r") as f:
        dungeon_map = list(list(line) for line in f.readlines())

    with open(DATA_GAME_DIALOGUE, "r") as g:
        import json

        game_text = json.load(g)

    TERM = Terminal()

    # Initialize this stuff.
    area_map = MapDisplay(term=TERM, map_ascii=dungeon_map)
    description = DescriptionDisplay(
        term=TERM, title="Hello!", text=game_text["introduction_0"]
    )
    options = OptionsDisplay(term=TERM, options=USER_INPUT_OPTIONS)
    line = LineDisplay(term=TERM)

    ui = UI(
        term=TERM,
        area_map=area_map,
        description=description,
        line=line,
        options=options,
    )

    ui.refresh_display()

    ui.wait_for_key()
    ui.wait_for_key()
    ui.wait_for_key()
    ui.wait_for_key()
