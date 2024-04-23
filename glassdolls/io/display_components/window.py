import curses

from attrs import define, field

from glassdolls.constants import ASCII_CODES
from glassdolls.utils import Loc


@define
class Window:
    loc_start: Loc = field(default=Loc(1, 1))
    height: int = field(default=1)
    width: int = field(default=30)
    border: int = field(default=1)
    border_color: int = field(default=0)
    subwindow: "curses._CursesWindow" = field(init=False, repr=False)

    def init_window(self) -> None:
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
