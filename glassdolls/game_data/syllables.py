from typing import TypeAlias

import numpy as np

with open("data/syllables_vowels.csv", "r", encoding="utf-8") as f:
    VOWELS = [line.strip() for line in f.readlines()]

with open("data/syllables_nonvowels.csv", "r", encoding="utf-8") as f:
    NONVOWELS = [line.strip() for line in f.readlines()]

SyllableList: TypeAlias = list[str]


def create_random_syllables(
    vowel_first_num: int = 25,
    nonvowel_first_num: int = 50,
    nonvowel_vowel_nonvowel_num: int = 10,
    vowel_nonvowel_vowel_num: int = 10,
) -> SyllableList:

    # Vowel first.
    vf_vowels = np.random.choice(VOWELS, vowel_first_num, replace=True)
    vf_nonvowels = np.random.choice(NONVOWELS, vowel_first_num, replace=True)
    vf_list = ["".join(i) for i in zip(vf_vowels, vf_nonvowels)]

    # Nonvowel first.
    nvf_nonvowels = np.random.choice(NONVOWELS, nonvowel_first_num, replace=True)
    nvf_vowels = np.random.choice(VOWELS, nonvowel_first_num, replace=True)
    nvf_list = ["".join(i) for i in zip(nvf_nonvowels, nvf_vowels)]

    # Nonvowel, Vowel, Nonvowel.
    nvn_nonvowels_0 = np.random.choice(
        NONVOWELS, nonvowel_vowel_nonvowel_num, replace=True
    )
    nvn_vowels = np.random.choice(VOWELS, nonvowel_vowel_nonvowel_num, replace=True)
    nvn_nonvowels_1 = np.random.choice(
        NONVOWELS, nonvowel_vowel_nonvowel_num, replace=True
    )
    nvn_list = ["".join(i) for i in zip(nvn_nonvowels_0, nvn_vowels, nvn_nonvowels_1)]

    # Vowel, Nonvowel, Vowel.
    vnv_vowels_0 = np.random.choice(VOWELS, vowel_nonvowel_vowel_num, replace=True)
    vnv_nonvowels = np.random.choice(NONVOWELS, vowel_nonvowel_vowel_num, replace=True)
    vnv_vowels_1 = np.random.choice(VOWELS, vowel_nonvowel_vowel_num, replace=True)
    vnv_list = ["".join(i) for i in zip(vnv_vowels_0, vnv_nonvowels, vnv_vowels_1)]

    # TODO: This gets approximate value...need to while loop it or something.

    return list(set(vf_list + nvf_list + nvn_list + vnv_list))
