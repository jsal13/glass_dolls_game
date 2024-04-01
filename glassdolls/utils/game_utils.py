from attrs import define


@define
class Loc:
    x: int
    y: int

    def __add__(self, other: "Loc") -> "Loc":
        return Loc(x=self.x + other.x, y=self.y + other.y)

    def astuple(self) -> tuple[int, int]:
        return (self.x, self.y)
