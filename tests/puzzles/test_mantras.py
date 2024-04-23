import numpy as np
import pytest

from glassdolls._types import MantraChantList
from glassdolls.puzzles.mantras import (generate_mantra,
                                        generate_random_syllables)


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


def test_generate_mantra_outputs_correctly(syllable_list: list[str]) -> None:
    mantra = generate_mantra(
        syllables_list=syllable_list,
        min_words_per_mantra=2,
        max_words_per_mantra=3,
    )

    assert mantra == "KJ WV"


def test_generate_random_syllables_outputs_correctly() -> None:
    syllables = generate_random_syllables(
        vowel_first_num=2,
        nonvowel_first_num=3,
        nonvowel_vowel_nonvowel_num=1,
        vowel_nonvowel_vowel_num=1,
    )
    assert sorted(syllables) == sorted(
        ["CLUU", "DJOY", "EEV", "IOCR", "KHYIKL", "SHUU", "UERWEE"]
    )


def test_generate_random_syllables_fails_with_too_few_syllables() -> None:

    with pytest.raises(ValueError):
        syllables = generate_random_syllables(
            vowel_first_num=10000,
            nonvowel_first_num=1,
            nonvowel_vowel_nonvowel_num=1,
            vowel_nonvowel_vowel_num=1,
        )
