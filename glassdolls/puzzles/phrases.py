import re

import numpy as np
from bs4 import BeautifulSoup

from glassdolls.constants import DATA_RANDOM_PHRASE_EN_XML


def get_phrase_list() -> list[str]:
    """Get list of phrases."""

    with open(DATA_RANDOM_PHRASE_EN_XML, "r", encoding="utf-8") as xml:
        soup = BeautifulSoup(xml, features="xml")

    # Removes the newlines and extra spaces from the text.
    return [
        re.sub(r"\n *", " ", phrase.get_text()).strip().upper()
        for phrase in soup.find_all("phrase")
    ]


def get_random_phrases(n: int) -> list[str]:
    all_phrases = get_phrase_list()
    num_phrases = len(all_phrases)
    return np.random.choice(all_phrases, n, replace=False).tolist()
