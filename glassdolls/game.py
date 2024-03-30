from attrs import define, field
from blessed import Terminal
from blinker import NamedSignal, signal

from glassdolls.constants import DATA_GAME_DIALOGUE, MAPS_DUNGEON_LEVEL_0_TXT
from glassdolls.io.input import UserInput
from glassdolls.io.output import GameScreen
from glassdolls.io.player import PlayerState
from glassdolls.io.signals import SignalSender


@define
class GameState:
    pass


@define
class Game(SignalSender):
    term: Terminal = field(repr=False)
    game_screen: GameScreen = field(repr=False)
    user_input: UserInput = field(repr=False)
    player: PlayerState = field(repr=False)

    signal_player_movement: NamedSignal = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.signal_player_movement = signal(
            f"{self.__class__.__name__}_player_movement"
        )

        # Subscribe to Signals.
        self.signal_player_movement.connect(self.player.handle_signal_player_movement)

        self.player.signal_player_loc_changed.connect(
            self.game_screen.handle_player_loc_changed
        )

        self.user_input.signal_player_movement.connect(
            self.player.handle_signal_player_movement
        )


if __name__ == "__main__":
    with open(MAPS_DUNGEON_LEVEL_0_TXT, "r") as f, open(DATA_GAME_DIALOGUE, "r") as g:
        import json

        dungeon_map = list(list(line) for line in f.readlines())
        game_text = json.load(g)

    TERM = Terminal()

    # Game Screen Init.
    game_screen = GameScreen(term=TERM)
    game_screen.area_map.map_ascii = dungeon_map
    game_screen.description.title = "Hello!"
    game_screen.description.text = game_text["introduction_0"]
    game_screen.refresh_display()

    # Game Init.
    user_input = UserInput(term=TERM)

    from glassdolls.io.utils import Loc

    player = PlayerState()
    player.loc = Loc(2, 2)
    game = Game(
        term=TERM, game_screen=game_screen, user_input=user_input, player=player
    )

    # Start the Game Stuff.
    game.user_input.wait_for_key()
    game.user_input.wait_for_key()
    # game.user_input.wait_for_key()
    # game.user_input.wait_for_key()
