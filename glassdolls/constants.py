import os
import dotenv

dotenv.load_dotenv()

DATA_SYLLABLE_FILE_LOC: str = os.getenv("DATA_SYLLABLE_FILE_LOC", "data/syllables.json")
DATA_SPELLS_FILE_LOC: str = os.getenv("DATA_SPELLS_FILE_LOC", "data/spells.json")
DATA_PRIMES_FILE_LOC: str = os.getenv("DATA_PRIMES_FILE_LOC", "data/primes.json")
DATA_RANDOM_PHRASE_EN_XML: str = os.getenv(
    "DATA_RANDOM_PHRASE_EN_XML", "data/random_phrases_en.xml"
)


MONGO_CONNECTION_STRING: str = os.getenv(
    "MONGO_CONNECTION_STRING", "mongodb://admin:example@localhost:27017"
)
PG_CONNECTION_STRING: str = os.getenv(
    "PG_CONNECTION_STRING", "postgresql://admin:example@localhost:5432"
)
