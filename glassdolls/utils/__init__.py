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
    
    def __eq__(self, other: "Loc") -> bool:
        return (self.x == other.x) & (self.y == other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))