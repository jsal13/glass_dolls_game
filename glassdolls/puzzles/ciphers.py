import string

import numpy as np

from glassdolls._types import TranslationTable, TranslationTableStrKey


def cesaer_cipher(text: str, shift_amount: int = 1) -> str:
    """
    Creates Cesaer ciphertext from ``text``, letters shifted by ``shift_amount``.

    Args:
        text (str): Plaintext to be encoded.
        shift_amount (int, optional): Number to shift the alphabet by. Defaults to 1.

    Returns:
        tuple[str, int]: (ciphertext, shift_amount)
    """
    translation_table = str.maketrans(
        string.ascii_uppercase,
        string.ascii_uppercase[shift_amount:] + string.ascii_uppercase[:shift_amount],
    )

    return text.upper().translate(translation_table)


def make_substitution_cipher_translation_table() -> TranslationTable:
    """Use a substitution cipher in ``text`` according to a random letter mapping."""

    return str.maketrans(
        dict(
            zip(
                list(string.ascii_uppercase),
                (np.random.permutation(list(string.ascii_uppercase))),
            )
        )
    )


def apply_substitution_cipher(text: str, translation_table: TranslationTable) -> str:
    """Use a substitution cipher in ``text`` according to a random letter mapping."""

    return text.translate(translation_table)


def translation_table_make_str_keys(
    translation_table: TranslationTable,
) -> TranslationTableStrKey:
    return {chr(k): v for k, v in translation_table.items()}
