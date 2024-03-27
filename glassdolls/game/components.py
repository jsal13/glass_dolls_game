from attrs import define, field
from blessed import Terminal

from glassdolls.game.map import GAME_AREAS, Area


@define
class Widget:
    term: Terminal

    def display(self) -> None:
        raise NotImplementedError


@define
class DescriptionWidget(Widget):
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
    area: Area = GAME_AREAS.dungeons["Start"]
    map_key: str = "0"

    def display(self) -> None:
        print(
            self.term.white(self.area.get_printable_revealed_map(map_key=self.map_key)),
            end="\n\n",
        )


@define
class InputWidget(Widget):
    prompt: list[str] = field(default=["?"])

    def display(self) -> None:
        for para in self.prompt:
            print(self.term.pink("\n".join(self.term.wrap(para))))


@define
class HorizontalRule(Widget):
    width: int = field(default=70)  # Default for wrap.

    def display(self) -> None:
        print(self.term.cyan("=" * self.width), "\n")
