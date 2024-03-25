from blessed import Terminal
from glassdolls.game.utils import refresh, wait_for_enter
from glassdolls.game.components import (
    DescriptionWidget,
    Widget,
    GameText,
    InputWidget,
    HorizontalRule,
    MapRenderWidget,
)
from glassdolls.game.map import GAME_AREAS

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

dungeon_0_level_0_screen = (
    MapRenderWidget(term=TERM, area=GAME_AREAS.dungeons["Start"], map_key="0"),
)


def render_screen(term: Terminal, screens: tuple[Widget, ...]) -> None:
    refresh(term=TERM)
    for screen in screens:
        screen.display()


def main(term: Terminal = TERM, text: GameText = TEXT) -> None:
    render_screen(term=TERM, screens=introduction_screen)
    wait_for_enter(term=TERM)

    render_screen(term=TERM, screens=sample_screen)
    wait_for_enter(term=TERM)

    render_screen(term=TERM, screens=dungeon_0_level_0_screen)
    wait_for_enter(term=TERM)


if __name__ == "__main__":
    main()
