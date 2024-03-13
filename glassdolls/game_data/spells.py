import json
import numpy as np
from typing import TypeAlias

from glassdolls.game_data.syllables import SyllableList

with open("data/spell_list.json", "r", encoding="utf-8") as f:
    SPELL_LIST = json.load(f)

SpellChantList: TypeAlias = dict[str, str]


def make_spells(
    syllables_list: SyllableList,
    spell_list: list[str],
    min_words_per_spell: int = 2,
    max_words_per_spell: int = 3,
) -> SpellChantList:

    # Make a list of syllables to use from the
    # "all syllables" list.
    syllables_to_use = np.random.choice(
        syllables_list, size=(max_words_per_spell * len(spell_list)), replace=False
    ).tolist()

    # Don't use a syllable more than once by popping.
    return {
        spell: " ".join(
            [
                syllables_to_use.pop()
                for i in range(
                    np.random.randint(min_words_per_spell, max_words_per_spell)
                )
            ]
        )
        for spell in spell_list
    }
