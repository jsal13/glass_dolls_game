from typing import Sequence, Any

from blinker import signal, Signal

from blessed import Terminal
from blessed.keyboard import Keystroke

from glassdolls.utils import Loc
from glassdolls.constants import MAPS_DUNGEON_LEVEL_0_TXT, DATA_GAME_DIALOGUE


#     # def render_and_wait_for_key(
#     #     self,
#     #     screens: Sequence["glassdolls.game.components.Widget"],
#     #     user_key: str | None = None,
#     # ) -> Keystroke:
#     #     """
#     #     Render and wait for user key.

#     #     Helper method combining ``.render`` and ``.wait_for_key``.
#     #     """
#     #     self.render(screens=screens)
#     #     return self.wait_for_key(user_key=user_key)

#     def wait_for_key(self, user_key: str | None = None) -> Keystroke:
#         """
#         Wait for user_input with value ``key``.

#         Notes
#         -----
#         See: https://blessed.readthedocs.io/en/latest/keyboard.html#keycodes

#         Args:
#             user_key (str | None, optional): Keycode for desired user key.  None will take any key. Defaults to None.
#         """
#         with self.term.cbreak():
#             while True:
#                 val = self.term.inkey()
#                 if val.is_sequence and ((user_key is None) or (val.name == user_key)):
#                     break
#         return val


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


class Display:
    def __init__(self, term: Terminal):
        self.term = term

    def print_at(self, x: int, y: int, text: str, color: str = "white") -> None:
        color_text: str

        if color == "white":
            color_text = self.term.white(text)
        elif color == "cyan":
            color_text = self.term.cyan(text)
        elif color == "navy":
            color_text = self.term.navy(text)
        else:
            raise ValueError(f"No such color {color} implemented.")

        print(self.term.move_xy(x=x, y=y) + color_text, end="")


class MapDisplay(Display):
    def __init__(self, term: Terminal, map_ascii: list[str]) -> None:
        self.term = term
        self.map_ascii = map_ascii

    def display(self) -> None:
        x, y = TERMINAL_XY_INIT_MAP.astuple()
        for jdx, row in enumerate(self.map_ascii):
            self.print_at(x=x, y=y + jdx, text=row)
        print()


class OptionsDisplay(Display):

    def __init__(
        self,
        term: Terminal,
        options: list[str] = USER_INPUT_OPTIONS,
    ) -> None:
        self.term = term
        self.options = options

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


class DescriptionDisplay(Display):
    def __init__(
        self, term: Terminal, title: str | None = None, text: str | None = None
    ) -> None:
        self.term = term
        self._title = title
        self._text = text

        # Signals
        self.signal_title_updated = signal("signal_title_updated")
        self.signal_text_updated = signal("signal_text_updated")

    @property
    def title(self) -> str | None:
        return self._title

    @title.setter
    def title(self, value: str | None) -> None:
        self._title = value
        self.signal_title_updated.send("signal_title_updated")

    @property
    def text(self) -> str | None:
        return self._text

    @text.setter
    def text(self, value: str | None) -> None:
        self._text = value
        self.signal_text_updated.send("signal_text_updated")

    def display(self, x: int, y: int) -> None:
        if self.title is not None:
            self.print_at(x=x, y=y, text=self.title, color="cyan")
            self.print_at(
                x=x, y=y + 1, text="-" * len(self.title) + "\n\n", color="cyan"
            )

        if self.text is not None:
            self.text_list = self.text.split("\n")
            y_offset = 2 if self.title is not None else 0
            for line in self.text_list:
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


class LineDisplay(Display):

    def vertical(self, x: int, y_min: int, y_max: int) -> None:
        for jdx in range(y_min, y_max + 1):
            self.print_at(x=x, y=jdx, text=ASCII_CODES["Vertical"], color="navy")

    def horizontal(self, y: int, x_min: int, x_max: int) -> None:
        for idx in range(x_min, x_max + 1):
            self.print_at(x=idx, y=y, text=ASCII_CODES["Horizontal"], color="navy")

    def crossing(self, x: int, y: int) -> None:
        self.print_at(
            x=x, y=y, text=ASCII_CODES["Up_Left_Right_Crossing"], color="navy"
        )


class UI:
    def __init__(
        self,
        term: Terminal,
        map_disp: MapDisplay,
        opt_disp: OptionsDisplay,
        line_disp: LineDisplay,
        descr_disp: DescriptionDisplay,
    ) -> None:
        self.term = term
        self.map = map_disp
        self.opt = opt_disp
        self.line = line_disp
        self.descr = descr_disp

        # Connect signals to subscriber.
        self.descr.signal_title_updated.connect(self.refresh_display)
        self.descr.signal_text_updated.connect(self.refresh_display)

    def _refresh_screen(self) -> None:
        print(f"{self.term.home}{self.term.clear}")

    def refresh_display(self, sender: Signal | None = None) -> None:
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
        self.map.display()

        self.opt.display(
            x=(TERMINAL_XY_INIT_MAP.x + MAP_WIDTH + HORIZ_PADDING + 1 + HORIZ_PADDING),
            y=VERT_PADDING,
        )
        self.descr.display(
            x=TERMINAL_XY_INIT_MAP.x,
            y=TERMINAL_XY_INIT_MAP.y + MAP_HEIGHT + (2 * VERT_PADDING + 1),
        )


if __name__ == "__main__":
    with open(MAPS_DUNGEON_LEVEL_0_TXT, "r") as f:
        dungeon_map = list(f.readlines())

    with open(DATA_GAME_DIALOGUE, "r") as g:
        import json

        game_text = json.load(g)

    TERM = Terminal()

    # Initialize this stuff.
    map_disp = MapDisplay(term=TERM, map_ascii=dungeon_map)
    descr_disp = DescriptionDisplay(
        term=TERM, title="Hello!", text=game_text["introduction_0"]
    )
    opt_disp = OptionsDisplay(term=TERM, options=USER_INPUT_OPTIONS)
    line_disp = LineDisplay(term=TERM)

    ui = UI(
        term=TERM,
        map_disp=map_disp,
        opt_disp=opt_disp,
        line_disp=line_disp,
        descr_disp=descr_disp,
    )

    ui.refresh_display()

    import time

    time.sleep(2)
    ui.descr.text = "WHATS UP BAYBEES."
    time.sleep(2)
    ui.descr.text = "WHATS UP RABIESSS."
