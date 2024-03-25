import json

from attrs import define, field
from blessed import Terminal

from glassdolls.constants import DATA_GAME_DIALOGUE
from glassdolls.game.map import GAME_AREAS, Area


@define
class Widget:
    term: Terminal

    def display(self) -> None:
        raise NotImplementedError


@define
class DescriptionWidget(Widget):
    term: Terminal
    title: str = field(default="Title")
    summary: list[str] = field(default=["Summary goes here."])

    def display(self) -> None:
        dash_width = len(self.title)
        print(self.term.cyan(self.title))
        print(self.term.cyan("-" * dash_width), end="\n\n")
        for para in self.summary:
            print("\n".join(self.term.wrap(para)))
            print()


@define
class MapRenderWidget(Widget):
    term: Terminal
    area: Area
    map_key: str

    def display(self) -> None:
        print(
            self.term.white("\n".join(self.area.maps[self.map_key]["revealed"])),
            end="\n\n",
        )


@define
class InputWidget(Widget):
    term: Terminal
    prompt: list[str] = field(default=["?"])

    def display(self) -> None:
        for para in self.prompt:
            print(self.term.pink("\n".join(self.term.wrap(para))))


@define
class HorizontalRule(Widget):
    term: Terminal
    width: int = field(default=70)  # Default for wrap.

    def display(self) -> None:
        print(self.term.cyan("=" * self.width), "\n")


class GameText:
    def __init__(self, game_text_path: str = DATA_GAME_DIALOGUE):
        with open(game_text_path, "r", encoding="utf-8") as f:
            self.text = json.load(f)

    def _get_text(self, key: str) -> list[str]:
        return self.text[key]

    def __getitem__(self, key: str) -> list[str]:
        return self._get_text(key=key)
