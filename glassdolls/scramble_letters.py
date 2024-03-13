import string
from typing import TypeAlias

import numpy as np

TranslationTable: TypeAlias = dict[int, str]


def _create_random_translation_table() -> TranslationTable:

    return str.maketrans(
        dict(
            zip(
                list(string.ascii_uppercase),
                (np.random.permutation(list(string.ascii_uppercase))),
            )
        )
    )


def scramble_letters(
    text: str, seed: int | None = None
) -> tuple[str, TranslationTable]:
    """Scramble letters in ``text`` according to a random letter mapping."""
    if isinstance(seed, int):
        np.random.seed(seed=seed)

    ttable = _create_random_translation_table()
    return (text.translate(ttable), ttable)


print(scramble_letters("WHATS THE FUSS ABOUT?", seed=10))
