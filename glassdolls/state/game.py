from typing import Any

from attrs import define, field

from glassdolls.state.player import PlayerState
from glassdolls.state.signals import SignalSender
from glassdolls.state.maps import MapState

from glassdolls import logger


@define
class GameState(SignalSender):
    player_state: PlayerState = field(repr=False, default=PlayerState())
    map_state: MapState = field(repr=False, default=MapState())

    def handle_signal_player_input_attempt_movement(
        self, signal: str | None = None, data: dict[str, Any] | None = None
    ) -> None:
        self._log_handle_signal(signal=signal, data=data)

        if data is not None:
            if data.get("direction") is not None:
                potential_loc = self.player_state.loc + data["direction"]
                if not self.map_state.is_collider(loc=potential_loc):
                    self.player_state.loc = potential_loc
            else:
                raise ValueError(f"Got {data}, not a dict with key 'direction'.")
        else:
            raise ValueError("Got empty data package.")
