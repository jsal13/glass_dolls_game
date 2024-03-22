import json
from typing import TypeAlias

import numpy as np


with (
    open("data/syllables.json", "r", encoding="utf-8") as syllable_json,
    open("data/spells.json", "r", encoding="utf-8") as spell_json,
):
    syllables = json.load(syllable_json)
    VOWELS = syllables["vowels"]
    NONVOWELS = syllables["nonvowels"]
    SPELL_LIST = json.load(spell_json)


SyllableList: TypeAlias = list[str]
SpellChantList: TypeAlias = dict[str, str]


def generate_random_syllables(
    vowel_first_num: int = 25,
    nonvowel_first_num: int = 50,
    nonvowel_vowel_nonvowel_num: int = 15,
    vowel_nonvowel_vowel_num: int = 10,
) -> SyllableList:
    """
    Generate Random Syllables for use in Spells.

    Args:
        vowel_first_num (int, optional): Number of vowel-first syllables. Defaults to 25.
        nonvowel_first_num (int, optional): Number of non-vowel-first syllables. Defaults to 50.
        nonvowel_vowel_nonvowel_num (int, optional): Number of non-vowel-vowel-non-vowel syllables. Defaults to 15.
        vowel_nonvowel_vowel_num (int, optional): Number of vowel-nonvowel-vowel syllables. Defaults to 10.

    Returns:
        SyllableList: List of syllables.  Note that this may be slightly less than the desired amount.
    """

    def _generate_n_syllables(arrs: list[list[str]], n: int) -> SyllableList:
        if (total_combos := np.prod([len(arr) for arr in arrs])) < n:
            raise ValueError(
                f"Cannot have {n} combinations, max combinations with current arrs is {total_combos}."
            )

        ACC_KILLSWITCH = 10000  # Doing this in case the while doesn't end.
        syllables: set[str] = set()
        acc = 0
        while (len(syllables) < n) and (acc < ACC_KILLSWITCH):
            acc += 1
            num_left = n - len(syllables)
            arrs_list = []
            for arr in arrs:
                arrs_list.append(
                    np.random.choice(arr, size=num_left, replace=True).tolist()
                )
            arrs_zipped = ["".join(syllable) for syllable in zip(*arrs_list)]
            syllables = syllables.union(arrs_zipped)

        return list(syllables)

    vn_list = _generate_n_syllables(arrs=[VOWELS, NONVOWELS], n=vowel_first_num)
    nv_list = _generate_n_syllables(arrs=[NONVOWELS, VOWELS], n=nonvowel_first_num)
    vnv_list = _generate_n_syllables(
        arrs=[VOWELS, NONVOWELS, VOWELS], n=vowel_nonvowel_vowel_num
    )
    nvn_list = _generate_n_syllables(
        arrs=[NONVOWELS, VOWELS, NONVOWELS], n=nonvowel_vowel_nonvowel_num
    )
    return vn_list + nv_list + nvn_list + vnv_list


def generate_spells(
    syllables_list: SyllableList,
    spell_list: dict[str, list[str]],
    min_words_per_spell: int = 2,
    max_words_per_spell: int = 3,
) -> SpellChantList:

    SPELL_LEVEL = "0"
    # Make a list of syllables to use from the
    # "all syllables" list.
    syllables_to_use = np.random.choice(
        syllables_list,
        size=(max_words_per_spell * len(spell_list[SPELL_LEVEL])),
        replace=False,
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
        for spell in spell_list[SPELL_LEVEL]
    }


rand = generate_spells(
    syllables_list=generate_random_syllables(), spell_list=SPELL_LIST
)
print(rand)
