class Loc:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "Loc") -> "Loc":
        return Loc(x=self.x + other.x, y=self.y + other.y)

    def astuple(self) -> tuple[int, int]:
        return (self.x, self.y)
