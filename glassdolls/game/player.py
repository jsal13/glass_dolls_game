from typing import Any

from attrs import define, field
from blinker import NamedSignal, signal

from glassdolls.game.signals import SignalSender
from glassdolls.utils import Loc


@define
class PlayerState(SignalSender):
    _loc: Loc = field(init=False)

    health: int = field(default=10)
    magic: int = field(default=0)
    strength: int = field(default=1)
    intelligence: int = field(default=1)

    signal_player_loc_changed: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.signal_player_loc_changed = signal(
            f"{self.__class__.__name__}_player_loc_changed"
        )

        # Initialize Loc.
        self.loc = Loc(0, 0)

    @property
    def loc(self) -> Loc:
        return self._loc

    @loc.setter
    def loc(self, value: Loc) -> None:
        self._loc = value
        self.send_signal(self.signal_player_loc_changed, data={"location": self.loc})

    def handle_signal_player_input_attempt_movement(
        self, signal: str | None = None, data: dict[str, Any] | None = None
    ) -> None:
        self._log_handle_signal(signal=signal, data=data)

        if data is not None:
            if data.get("direction") is not None:
                self.loc += data["direction"]
            else:
                raise ValueError(f"Got {data}, not a dict with key 'direction'.")
        else:
            raise ValueError("Got empty data package.")
