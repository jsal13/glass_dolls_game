import sys
from typing import Any

from attrs import define, field
from blessed import Terminal
from blinker import NamedSignal, signal

from glassdolls import logger
from glassdolls.signals import SignalSender
from glassdolls.output import GameScreen
from glassdolls.input import UserInput
from glassdolls.player import PlayerState
from glassdolls.constants import (
    USER_MOVEMENT,
    MAPS_DUNGEON_LEVEL_0_TXT,
    DATA_GAME_DIALOGUE,
)


@define
class GameState:
    pass


@define
class Game(SignalSender):
    term: Terminal = field(repr=False)
    game_screen: GameScreen = field(repr=False)
    user_input: UserInput = field(repr=False)
    player: PlayerState = field(repr=False)

    # Signals.
    signal_user_input: NamedSignal = field(init=False, repr=False)
    signal_player_movement: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.signal_user_input = signal(f"{self.__class__.__name__}_user_input")
        self.signal_player_movement = signal(
            f"{self.__class__.__name__}_player_movement"
        )

        # Subscribe to Signals.
        self.user_input.signal_user_input.connect(self.handle_signal_user_input)
        self.signal_player_movement.connect(self.player.handle_signal_player_movement)

    def handle_signal_user_input(
        self, signal: str | None = None, data: dict[str, Any] | None = None
    ) -> None:
        self._log_handle_signal(signal=signal, data=data)

        if data is not None:
            if (user_key := data["key"]) is not None:
                logger.debug(f"User hit {user_key} key.")

                if user_key in ["KEY_LEFT", "KEY_RIGHT" "KEY_DOWN", "KEY_UP"]:
                    player_movement = USER_MOVEMENT[data["key"]]
                    self.send_signal(
                        self.signal_player_movement, data={"direction": player_movement}
                    )

                elif data["key"] == "Q":
                    sys.exit(0)

        else:
            raise ValueError("Got empty data package.")


if __name__ == "__main__":
    with open(MAPS_DUNGEON_LEVEL_0_TXT, "r") as f, open(DATA_GAME_DIALOGUE, "r") as g:
        import json

        dungeon_map = list(list(line) for line in f.readlines())
        game_text = json.load(g)

    TERM = Terminal()

    game_screen = GameScreen(term=TERM)
    game_screen.area_map.map_ascii = dungeon_map
    game_screen.description.title = "Hello!"
    game_screen.description.text = game_text["introduction_0"]

    game_screen.refresh_display()
