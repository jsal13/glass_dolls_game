import curses
from typing import Any

from attrs import define, field

from glassdolls.io.input import UserInput
from glassdolls.io.output import GameScreen, GameText, MapDisplay, DescriptionDisplay, InputWindow
from glassdolls.io.game import Game, GameState

from glassdolls.game.player import PlayerState
from glassdolls.game.maps import MapState
from glassdolls.game.events import Events, Event
from glassdolls.utils import Loc

from glassdolls import logger
from glassdolls.io.utils import Color
from glassdolls.constants import TERMINAL_XY_INIT_MAP, MAP_HEIGHT, MAP_WIDTH, MAP_TOWN_TEST_FILE, HORIZ_PADDING, VERT_PADDING, DESCRIPTION_HEIGHT, MAX_SCREEN_WIDTH

PLAYER_COLOR = "CYAN"
DESC_TITLE_COLOR = "CYAN"
DESC_TEXT_COLOR = "WHITE"
OPTIONS_TITLE_COLOR = "CYAN"
OPTIONS_TEXT_COLOR = "WHITE"
LINE_COLOR = "YELLOW"
DUNGEON_WALL_COLOR = "WHITE"
INPUT_BORDER_COLOR = "CYAN"

if __name__ == "__main__":
    
    def run(term: "curses._CursesWindow") -> None:
        import time
        color = Color()

        # Text, Towns, Dungeons.
        game_text = GameText()

        # Events, Map, and Player States.
        events = Events(data={Loc(5, 3): Event(loc=Loc(5, 3))})  # Initial events.
        map_state = MapState(events=events, map_file=MAP_TOWN_TEST_FILE)
        player_state = PlayerState()

        # Join Player + Map states together so they can communicate nicely.
        game_state = GameState(player_state=player_state, map_state=map_state)

        # Terminal Output Classes
        map_display = MapDisplay(
                    loc_start=TERMINAL_XY_INIT_MAP,
                    map_state=map_state,
                    height=MAP_HEIGHT,
                    width=MAP_WIDTH,
                    border=0,
                    border_color=0,
                    map_color=color[DUNGEON_WALL_COLOR],
                    player_color=color[PLAYER_COLOR],
                )
        
        options = DescriptionDisplay(
            loc_start=TERMINAL_XY_INIT_MAP + Loc(MAP_WIDTH + (2 * HORIZ_PADDING), 0),
            height=MAP_HEIGHT,
            width=20,
            border=0,
            border_color=0,
            text_color=color[OPTIONS_TEXT_COLOR],
            title_color=color[OPTIONS_TITLE_COLOR],
        )

        description = DescriptionDisplay(
            loc_start=TERMINAL_XY_INIT_MAP + Loc(0, MAP_HEIGHT + (2 * VERT_PADDING)),
            height=DESCRIPTION_HEIGHT,
            width=MAX_SCREEN_WIDTH,
            border=0,
            border_color=0,
            text_color=color[DESC_TEXT_COLOR],
            title_color=color[DESC_TITLE_COLOR],
        )

        input_window = InputWindow(
            loc_start=Loc(
                TERMINAL_XY_INIT_MAP.x,
                TERMINAL_XY_INIT_MAP.y
                + MAP_HEIGHT
                + (2 * VERT_PADDING)
                + DESCRIPTION_HEIGHT
                + VERT_PADDING,
            ),
            height=1,
            width=MAX_SCREEN_WIDTH - 5,
            border=1,
            border_color=color[INPUT_BORDER_COLOR],
        )

        # Combines windows into the terminal output screen.
        game_screen = GameScreen(term=term, color=color, map_display=map_display, options=options, description=description, input_window=input_window)

        # game_screen.draw_lines()
        # game_screen.options.display()
        user_input = UserInput()

        game = Game(
            term=term, game_screen=game_screen, user_input=user_input, game_state=game_state
        )

        # GAME STATE AND DISPLAY COMPLETE, INITIALIZING VALUES.
        # (Must come after `Game` init.)
        player_state.loc = Loc(2, 2)
        game_screen.description.title = "Hello!"
            

        # intro_text = game_text.text["introduction"]
        # if isinstance(intro_text, str):
        #     raise ValueError("Expected a list for `intro_text`.")
        # game_screen.description.display_dialogue(text_list=intro_text)

        # usr_input = game_screen.input_window.create_user_input()

        # Start the Game and wait for the user.
        while True:
            game.user_input.wait_for_key()

    # curses.wrapper rapper calls "noecho, cbreak, keypad=True" on call.
    curses.wrapper(run)
