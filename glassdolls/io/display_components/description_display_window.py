import textwrap
from attrs import define, field

import curses

from glassdolls.state.events import Event
from glassdolls.io.display_components.window import Window
from glassdolls.constants import MAX_SCREEN_WIDTH


@define
class DescriptionDisplay(Window):
    _title: str = field(default="")
    _text: str = field(default="")
    title_color: int = field(default=256)
    text_color: int = field(default=0)

    def __attrs_post_init__(self) -> None:
        self.init_window()

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

    def handle_player_found_event(self, event: Event) -> None:
        self.title = event.make_title()
        self.text = event.make_body()

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
