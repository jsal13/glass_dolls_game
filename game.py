from blessed import Terminal
from utils import refresh, wait_for_enter
from components import DescriptionWidget, Widget, GameText, InputWidget, HorizontalRule

TERM = Terminal()
TEXT = GameText()

introduction_screen = (
    DescriptionWidget(term=TERM, title="Welcome!", summary=TEXT["introduction"]),
    HorizontalRule(term=TERM),
    InputWidget(term=TERM, prompt=TEXT["continue"]),
)

sample_screen = (
    DescriptionWidget(term=TERM, title="Sample!", summary=TEXT["sample"]),
    HorizontalRule(term=TERM),
    InputWidget(term=TERM, prompt=TEXT["continue"]),
)


def render_screen(term: Terminal, screens: tuple[Widget, ...]):
    refresh(term=TERM)
    for screen in screens:
        screen.display()


def main(term=TERM, text=TEXT) -> None:

    render_screen(term=TERM, screens=introduction_screen)
    wait_for_enter(term=TERM)

    render_screen(term=TERM, screens=sample_screen)
    wait_for_enter(term=TERM)


if __name__ == "__main__":
    main()
