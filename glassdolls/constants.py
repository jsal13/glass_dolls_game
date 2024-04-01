import os
import json
import dotenv

from glassdolls._types import MapTiles
from glassdolls.utils import Loc

dotenv.load_dotenv()


# GENERAL DATA
DATA_DIR = os.getenv("DATA_DIR", "data")
DATA_SYLLABLE_FILE_LOC: str = os.getenv(
    "DATA_SYLLABLE_FILE_LOC", f"{DATA_DIR}/syllables.json"
)
DATA_SPELLS_FILE_LOC: str = os.getenv("DATA_SPELLS_FILE_LOC", f"{DATA_DIR}/spells.json")
DATA_PRIMES_FILE_LOC: str = os.getenv("DATA_PRIMES_FILE_LOC", f"{DATA_DIR}/primes.json")
DATA_RANDOM_PHRASE_EN_XML: str = os.getenv(
    "DATA_RANDOM_PHRASE_EN_XML", f"{DATA_DIR}/random_phrases_en.xml"
)

# DIALOGUE AND TEXT
DATA_GAME_DIALOGUE: str = os.getenv("DATA_GAME_DIALOGUE", "data/game_text.json")

# MAPS
MAP_DIR = os.getenv("MAP_DIR", "data/maps")
MAP_LEGEND_JSON_FILE = os.getenv("MAP_LEGEND_JSON", f"{MAP_DIR}/map_legend.json")

with open(MAP_LEGEND_JSON_FILE, "r", encoding="utf-8") as map_legend_json:
    MAP_LEGEND_JSON: dict[str, dict[str, str]] = json.load(map_legend_json)

# How do we do typehints on this stuff from, say, the map file?
MAP_DUNGEON_LEVEL_0_TXT_FILE = os.getenv(
    "MAP_DUNGEON_LEVEL_0_TXT", f"{MAP_DIR}/dungeon_level_0.txt"
)

with open(MAP_DUNGEON_LEVEL_0_TXT_FILE, "r", encoding="utf-8") as dungeon_level_0:
    MAP_DUNGEON_LEVEL_0_TXT: MapTiles = [
        list(row) for row in dungeon_level_0.readlines()
    ]


# DB
MONGO_CONNECTION_STRING: str = os.getenv(
    "MONGO_CONNECTION_STRING", "mongodb://admin:example@localhost:27017"
)
PG_CONNECTION_STRING: str = os.getenv(
    "PG_CONNECTION_STRING", "postgresql://admin:example@localhost:5432"
)

# PUZZLE METADATA
DIFFICULTY_RANK = {
    "ciphers": {"substitution": "Medium", "cesaer": "Easy"},
    "math": {
        "sums": "Easy",
        "products": "Easy",
        "small prime factors": "Easy",
        "large prime factors": "Medium",
    },
}

# COLORS
# Ref: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
# COLOR_TO_ANSI = {
#     "black": 0,
#     "red": 1,
#     "green": 2,
#     "yellow": 3,
#     "blue": 4,
#     "purple": 5,
#     "cyan": 6,
#     "white": 7,
#     "hi_black": 8,
#     "hi_red": 9,
#     "hi_green": 10,
#     "hi_yellow": 11,
#     "hi_blue": 12,
#     "hi_purple": 13,
#     "hi_cyan": 14,
#     "hi_white": 15,
# }

# USER_COLOR = "hi_purple"
# DESC_TITLE_COLOR = "cyan"
# DESC_TEXT_COLOR = "white"
# OPTIONS_TITLE_COLOR = "cyan"
# OPTIONS_TEXT_COLOR = "white"
# LINE_COLOR = "hi_red"
# DUNGEON_WALL_COLOR = "white"

# DISPLAY CONSTANTS
HORIZ_PADDING = 2
VERT_PADDING = 1
MAX_SCREEN_WIDTH = 80
MAP_WIDTH = 16
MAP_HEIGHT = 16
DESCRIPTION_HEIGHT = 10
TERMINAL_XY_INIT_MAP = Loc(1 + HORIZ_PADDING, 1 + VERT_PADDING)  # Upper-left.

ASCII_CODES = {
    "Vertical": "║",
    "Horizontal": "═",
    "Crossing": "╬",
    "ULR_Crossing": "╩",
    "UL_Corner": "╔",
    "BL_Corner": "╚",
    "UR_Corner": "╗",
    "BR_Corner": "╝",
}

# USER CONSTANTS
USER_MOVEMENT = {
    "j": Loc(-1, 0),
    "l": Loc(1, 0),
    "k": Loc(0, 1),
    "i": Loc(0, -1),
}

# "KEY_LEFT": Loc(-1, 0),
# "KEY_RIGHT": Loc(1, 0),
# "KEY_DOWN": Loc(0, 1),
# "KEY_UP": Loc(0, -1),
