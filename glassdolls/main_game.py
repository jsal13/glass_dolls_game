import curses
import threading

from glassdolls import logger
from glassdolls.constants import (
    DESCRIPTION_HEIGHT,
    HORIZ_PADDING,
    MAP_HEIGHT,
    MAP_TOWN_TEST_FILE,
    MAP_WIDTH,
    MAX_SCREEN_WIDTH,
    TERMINAL_XY_INIT_MAP,
    USER_INPUT_OPTIONS,
    VERT_PADDING,
)
from glassdolls.game_data.data_init import Initializer
from glassdolls.game_data.game_text import GameText
from glassdolls.io.display_components.description_display_window import (
    DescriptionDisplay,
)
from glassdolls.io.display_components.input_window import InputWindow
from glassdolls.io.display_components.map_window import MapDisplay
from glassdolls.io.game_screen import GameScreen
from glassdolls.io.input import UserInput
from glassdolls.io.utils import get_color_map
from glassdolls.state.events import Event, Events
from glassdolls.state.game import Game
from glassdolls.state.map import MapState
from glassdolls.state.player import PlayerState
from glassdolls.utils import Loc
from glassdolls.game_data.factions import Faction

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
        # Initialize Data.
        # TODO: What if we don't care about this?  Can we turn it off?
        # GAME
        FACTIONS = [
            Faction.create_faction(name="Hemlock", element="Dark"),
            Faction.create_faction(name="Dawnstar", element="Light"),
            Faction.create_faction(name="Sunfall", element="Ice"),
            Faction.create_faction(name="Galeweaver", element="Wind"),
        ]

        initializer = Initializer(factions=FACTIONS)
        initializer.initialize()
        factions = initializer.factions

        color_map = get_color_map()

        # Text, Towns, Dungeons.
        game_text = GameText.create_gametext()

        # Events, Map, and Player States.
        event_metadata = factions[0].phrases[0]
        sample_event = Event(code=event_metadata["code"])
        events = Events(data={Loc(5, 3): sample_event})  # Initial events.
        map_state = MapState.create_mapstate(events=events, map_file=MAP_TOWN_TEST_FILE)
        player_state = PlayerState.create_default_playerstate()

        # Terminal Output Classes
        map_display = MapDisplay(
            loc_start=TERMINAL_XY_INIT_MAP,
            map_state=map_state,
            height=MAP_HEIGHT,
            width=MAP_WIDTH,
            border=0,
            border_color=0,
            map_color=color_map[DUNGEON_WALL_COLOR],
            player_color=color_map[PLAYER_COLOR],
        )

        options = DescriptionDisplay(
            loc_start=TERMINAL_XY_INIT_MAP + Loc(MAP_WIDTH + (2 * HORIZ_PADDING), 0),
            height=MAP_HEIGHT,
            width=20,
            border=0,
            border_color=0,
            text_color=color_map[OPTIONS_TEXT_COLOR],
            title_color=color_map[OPTIONS_TITLE_COLOR],
        )
        options.title = "Options"
        options.text = USER_INPUT_OPTIONS

        description = DescriptionDisplay(
            loc_start=TERMINAL_XY_INIT_MAP + Loc(0, MAP_HEIGHT + (2 * VERT_PADDING)),
            height=DESCRIPTION_HEIGHT,
            width=MAX_SCREEN_WIDTH,
            border=0,
            border_color=0,
            text_color=color_map[DESC_TEXT_COLOR],
            title_color=color_map[DESC_TITLE_COLOR],
        )
        description.title = "Hello!"

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
            border_color=color_map[INPUT_BORDER_COLOR],
        )

        # Combines windows into the terminal output screen.
        game_screen = GameScreen(
            term=term,
            color_map=color_map,
            map_display=map_display,
            options=options,
            description=description,
            input_window=input_window,
        )

        user_input = UserInput.create_user_input()

        game = Game.create_game(
            term=term,
            game_screen=game_screen,
            user_input=user_input,
            map_state=map_state,
            player_state=player_state,
        )

        # TODO: Can I put this into init?
        game.consumer.start_thread(callback=game.triage)

        # GAME STATE AND DISPLAY COMPLETE, INITIALIZING VALUES.
        # (Must come after `Game` init.)
        game.game_screen.map_display.display()
        game.player_state.loc = Loc(3, 1)

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
