import re
from bs4 import BeautifulSoup
import psycopg

DATA_RANDOM_PHRASE_EN_XML = "data/random_phrases_en.xml"


def get_phrase_list() -> list[str]:
    """Get list of phrases."""

    with open(DATA_RANDOM_PHRASE_EN_XML, "r", encoding="utf-8") as xml:
        soup = BeautifulSoup(xml, features="xml")

    # Removes the newlines and extra spaces from the text.
    return [
        re.sub(r"\n *", " ", phrase.get_text()).strip().upper()
        for phrase in soup.find_all("phrase")
    ]


def insert_phrase_data() -> None:
    """Insert Phrase list into Table."""
    with psycopg.connect(
        host="0.0.0.0",
        port="5432",
        dbname="admin",
        user="admin",
        password="example",
    ) as conn:
        with conn.cursor() as cur:
            for phrase in get_phrase_list():
                cur.execute(
                    "INSERT INTO random_phrases_en (phrase) VALUES (%(phrase)s)",
                    {"phrase": phrase},
                )
            conn.commit()


if __name__ == "__main__":
    insert_phrase_data()
