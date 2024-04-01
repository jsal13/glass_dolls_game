import json
from typing import Any

from attrs import define, field


@define
class Loc:
    x: int
    y: int

    def __add__(self, other: "Loc") -> "Loc":
        return Loc(x=self.x + other.x, y=self.y + other.y)

    def astuple(self) -> tuple[int, int]:
        return (self.x, self.y)


@define
class GameText:
    game_test_path: str
    text: dict[str, Any] = field(repr=False, init=False)

    def __init__(self, game_text_path: str):
        with open(game_text_path, "r", encoding="utf-8") as f:
            self.text = json.load(f)

    def __getitem__(self, key: str) -> list[str]:
        return self.text[key]
