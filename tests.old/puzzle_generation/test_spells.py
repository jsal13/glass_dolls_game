import numpy as np
import pytest

from glassdolls.puzzles.mantras import (
    MantraChantList,
    generate_random_syllables,
    generate_spells,
)


@pytest.fixture()
def syllable_list() -> list[str]:
    return [
        "ABC",
        "DEF",
        "GH",
        "IJ",
        "KL",
        "MNO",
        "P",
        "Q",
        "R",
        "ST",
        "UV",
        "W",
        "X",
        "Y",
        "Z",
        "ZY",
        "X",
        "WV",
        "U",
        "TS",
        "RQ",
        "PON",
        "ML",
        "KJ",
        "IH",
    ]


@pytest.fixture()
def spell_list() -> dict[str, list[str]]:
    return {"0": ["Fire", "Ice", "Wind", "Water", "Earth"]}


@pytest.fixture()
def spell_chant_list() -> MantraChantList:
    return {
        "Fire": "RQ KJ",
        "Ice": "UV ML",
        "Wind": "Y R",
        "Water": "ABC KL",
        "Earth": "MNO U",
    }


def test_generate_spells_outputs_correctly(
    syllable_list: list[str],
    spell_list: dict[str, list[str]],
    spell_chant_list: MantraChantList,
) -> None:
    spells = generate_spells(
        syllables_list=syllable_list,
        spell_list=spell_list,
        min_words_per_spell=2,
        max_words_per_spell=3,
    )

    assert spells == spell_chant_list


# def test_generate_spells_does_min_max_correctly(
#     syllable_list: list[str], spell_list: dict[str, list[str]]
# ) -> None:
#     min_words = 1
#     max_words = 5
#     spells = generate_spells(
#         syllables_list=syllable_list,
#         spell_list=spell_list,
#         min_words_per_spell=min_words,
#         max_words_per_spell=max_words,
#     )

# for spell, chant in spells.items():
#     print(chant.split(" "))
#     assert min_words <= len(chant.split(" ")) <= max_words


def test_generate_random_syllables_outputs_correctly() -> None:
    syllables = generate_random_syllables(
        vowel_first_num=2,
        nonvowel_first_num=3,
        nonvowel_vowel_nonvowel_num=1,
        vowel_nonvowel_vowel_num=1,
    )
    assert sorted(syllables) == sorted(
        ["CLU", "DJU", "ISZA", "OCR", "RWIKH", "SHO", "YV"]
    )


def test_generate_random_syllables_fails_with_too_few_syllables() -> None:

    with pytest.raises(ValueError):
        syllables = generate_random_syllables(
            vowel_first_num=10000,
            nonvowel_first_num=1,
            nonvowel_vowel_nonvowel_num=1,
            vowel_nonvowel_vowel_num=1,
        )
