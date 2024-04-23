import curses

from attrs import define, field

from glassdolls.io.display_components.window import Window


@define
class InputWindow(Window):

    cursor: str | None = field(default=">")

    def __attrs_post_init__(self) -> None:
        self.init_window()
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
