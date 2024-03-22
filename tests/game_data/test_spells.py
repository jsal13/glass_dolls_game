import pytest
import numpy as np

from glassdolls.game_data.spells import generate_spells, SpellChantList


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


def test_generate_spells_outputs_correctly(
    syllable_list: list[str], spell_list: dict[str, list[str]]
) -> None:
    np.random.seed(1234)
    spells = generate_spells(
        syllables_list=syllable_list,
        spell_list=spell_list,
        min_words_per_spell=2,
        max_words_per_spell=3,
    )

    expected: SpellChantList = {
        "Fire": "RQ KJ",
        "Ice": "UV ML",
        "Wind": "Y R",
        "Water": "ABC KL",
        "Earth": "MNO U",
    }

    assert spells == expected


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
