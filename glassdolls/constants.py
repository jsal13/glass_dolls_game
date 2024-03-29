import os
import dotenv

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
MAPS_DIR = os.getenv("MAPS_DIR", "data/maps")
MAPS_LEGEND_JSON = os.getenv("MAPS_LEGEND_JSON", f"{MAPS_DIR}/map_legend.json")
MAPS_DUNGEON_LEVEL_0_TXT = os.getenv(
    "MAPS_DUNGEON_LEVEL_0_TXT", f"{MAPS_DIR}/dungeon_level_0.txt"
)

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
