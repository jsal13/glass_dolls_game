import string
from typing import TypeAlias

import numpy as np

TranslationTable: TypeAlias = dict[int, str]
TranslationTableStrKey: TypeAlias = dict[str, str]


def substitution_cipher(text: str) -> tuple[str, TranslationTable]:
    """Use a substition cipher in ``text`` according to a random letter mapping."""

    trans_table: TranslationTable = str.maketrans(
        dict(
            zip(
                list(string.ascii_uppercase),
                (np.random.permutation(list(string.ascii_uppercase))),
            )
        )
    )

    return (text.translate(trans_table), trans_table)


def translation_table_make_str_keys(
    translation_table: TranslationTable,
) -> TranslationTableStrKey:
    return {chr(k): v for k, v in translation_table.items()}
