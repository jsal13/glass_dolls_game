import curses

from attrs import define, field

# from blinker import NamedSignal, signal

from glassdolls.io.input import UserInput
from glassdolls.io.output import GameScreen, GameText
from glassdolls.game.player import PlayerState
from glassdolls.game.signals import SignalSender
from glassdolls.utils import Loc
from glassdolls import logger
from glassdolls.io.utils import Color


@define
class GameState:
    pass


@define
class Game(SignalSender):
    term: "curses._CursesWindow" = field(repr=False)
    game_screen: GameScreen = field(repr=False)
    user_input: UserInput = field(repr=False)
    player: PlayerState = field(repr=False)

    def __attrs_post_init__(self) -> None:
        # Subscribe to Signals.

        # Updates map if player loc has changed.
        self.player.signal_player_loc_changed.connect(
            self.game_screen.area_map.handle_player_loc_changed
        )

        # Handles player movement if arrow is pressed.
        self.user_input.signal_player_input_movement.connect(
            self.player.handle_signal_player_input_movement
        )


if __name__ == "__main__":
    import time

    def run(term: "curses._CursesWindow") -> None:
        color = Color()
        game_text = GameText()

        # Initialize Game States, Screen, Input.
        player = PlayerState()
        game_screen = GameScreen(term=term, color=color)
        game_screen.draw_lines()
        game_screen.options.display()
        user_input = UserInput()

        game = Game(
            term=term, game_screen=game_screen, user_input=user_input, player=player
        )

        # INITIALIZE VALUES.  (Must come after `Game` init.)
        player.loc = Loc(2, 2)

        game_screen.description.title = "Hello!"
        # SIGNALS LATER.

        intro_text = game_text.text["introduction"]
        if isinstance(intro_text, str):
            raise ValueError("Expected a list for `intro_text`.")
        game_screen.description.display_dialogue(text_list=intro_text)

        usr_input = game_screen.input_window.create_user_input()

        # Start the Game Stuff.
        while True:
            game.user_input.wait_for_key()

    # curses.wrapper rapper calls "noecho, cbreak, keypad=True" on call.
    curses.wrapper(run)
