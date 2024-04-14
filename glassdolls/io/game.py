import curses
from typing import Any

from attrs import define, field

from glassdolls.io.input import UserInput
from glassdolls.io.output import GameScreen, GameText
from glassdolls.game.player import PlayerState
from glassdolls.game.signals import SignalSender
from glassdolls.game.maps import MapState
from glassdolls.game.events import Events, Event
from glassdolls.utils import Loc

from glassdolls import logger
from glassdolls.io.utils import Color


@define
class GameState(SignalSender):
    player_state: PlayerState = field(repr=False)
    map_state: MapState = field(repr=False)

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


@define
class Game(SignalSender):
    term: "curses._CursesWindow" = field(repr=False)
    game_screen: GameScreen = field(repr=False)
    user_input: UserInput = field(repr=False)
    game_state: GameState = field(repr=False)

    def __attrs_post_init__(self) -> None:
        # Updates map if player loc has changed.
        self.game_state.player_state.signal_player_loc_changed.connect(
            self.game_screen.map_display.handle_player_loc_changed
        )

        # Handles player movement if arrow is pressed.
        self.user_input.signal_player_input_attempt_movement.connect(
            self.game_state.handle_signal_player_input_attempt_movement
        )
