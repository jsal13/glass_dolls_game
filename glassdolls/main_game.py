import curses

from attrs import define, field
from blinker import NamedSignal, signal

from glassdolls.constants import MAPS_DUNGEON_LEVEL_0_TXT
from glassdolls.io.input import UserInput
from glassdolls.io.output import GameScreen
from glassdolls.game.player import PlayerState
from glassdolls.game.signals import SignalSender
from glassdolls.utils.game_utils import Loc, GameText
from glassdolls import logger


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
        self.player.signal_player_loc_changed.connect(
            self.game_screen.area_map.handle_player_loc_changed
        )

        self.user_input.signal_player_input_movement.connect(
            self.player.handle_signal_player_input_movement
        )


if __name__ == "__main__":
    import time

    def _init_colors() -> dict[str, int]:
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        color_map = {
            "WHITE_ON_BLACK": curses.color_pair(0),
            "CYAN_ON_BLACK": curses.color_pair(1),
            "RED_ON_BLACK": curses.color_pair(2),
            "RED_ON_WHITE": curses.color_pair(3),
        }

        return color_map

    def run(term: "curses._CursesWindow") -> None:

        #     # input_win = InputWindow(

        #     #     loc_start=Loc(10, 10),
        #     #     height=1,
        #     #     width=30,
        #     #     cursor=">",
        #     #     border_color=COLOR_MAP["CYAN_ON_BLACK"],
        #     # )
        #     # msg = input_win.create_user_input()

        # if __name__ == "__main__":
        #     # curses.wrapper rapper calls "noecho, cbreak, keypad=True" on call.
        #     curses.wrapper(main_display)

        logger.debug(str(_init_colors()))

        # Initialize Game States, Screen, Input.
        player = PlayerState()
        game_screen = GameScreen(term=term)
        game_screen.draw_lines()

        user_input = UserInput(term=term)

        game = Game(
            term=term, game_screen=game_screen, user_input=user_input, player=player
        )

        # Initialize Values.  Must come after _all_ ``Game`` items,
        # as ``Game`` connects the signals to the handlers.
        player.loc = Loc(2, 2)

        # game_screen.description.title = "Hello!"
        # game_screen.description.text = game_text["introduction_0"]
        # game_screen.refresh_display()

        # time.sleep(2)
        # Start the Game Stuff.
        while True:
            game.user_input.wait_for_key()

    # curses.wrapper rapper calls "noecho, cbreak, keypad=True" on call.
    curses.wrapper(run)
