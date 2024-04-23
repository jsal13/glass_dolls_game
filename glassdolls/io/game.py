import curses
from typing import Any

from attrs import define, field

from glassdolls import logger
from glassdolls.io.input import UserInput
from glassdolls.io.output import GameScreen
from glassdolls.state.events import Event
from glassdolls.state.game import GameState
from glassdolls.state.signals import SignalSender


@define
class Game(SignalSender):
    term: "curses._CursesWindow" = field(repr=False)
    game_screen: GameScreen = field(repr=False, default=GameScreen())
    user_input: UserInput = field(repr=False, default=UserInput())
    game_state: GameState = field(repr=False, default=GameState())

    def __attrs_post_init__(self) -> None:
        self.game_screen.draw_lines()
        self.game_screen.term.refresh()

        # Handles player movement if arrow is pressed.
        self.user_input.signal_player_input_attempt_movement.connect(
            self.game_state.handle_signal_player_input_attempt_movement
        )  # Connect Input -> Player

        # Handles player "look" action.
        self.user_input.signal_player_input_attempt_look.connect(
            self.game_state.player_state.handle_signal_player_input_attempt_look
        )  # Connect Input -> Player
        self.game_state.player_state.signal_player_look.connect(
            self.game_state.map_state.handle_signal_player_look
        )  # Connect Player -> Map State (Events)
        self.game_state.map_state.signal_player_looked_at_event.connect(
            self.handle_signal_player_looked_at_event
        )

    def handle_signal_player_looked_at_event(
        self, signal: str | None = None, data: dict[str, Any] | None = None
    ) -> None:
        self._log_handle_signal(signal=signal, data=data)

        if data is not None:
            event = data.get("event")
            if (event is not None) and (isinstance(event, Event)):
                self.game_screen.description.title = event.make_title()
                self.game_screen.description.text = event.make_body()

            else:
                raise ValueError(
                    f"Got {data}, not a dict with key 'event' of type Event."
                )
        else:
            raise ValueError("Got empty data package.")
