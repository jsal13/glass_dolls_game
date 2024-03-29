from typing import Any

from attrs import define
from blinker import Signal

from glassdolls import logger


@define
class Loc:
    x: int
    y: int

    def __add__(self, other: "Loc") -> "Loc":
        return Loc(x=self.x + other.x, y=self.y + other.y)

    def astuple(self) -> tuple[int, int]:
        return (self.x, self.y)


def send_signal(signal: Signal, data: dict[str, Any] | None = None) -> None:
    logger.debug(f"Sending {signal.__repr__()} with data: {data}")
    if data is not None:
        signal.send(signal.__repr__(), data=data)
    else:
        signal.send(signal.__repr__())
