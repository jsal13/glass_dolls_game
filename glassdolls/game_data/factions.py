from typing import Any
from attrs import define, field
from glassdolls.puzzles import basic_math, ciphers, mantras, phrases
from glassdolls._types import TranslationTableStrKey, TranslationTable

NUM_PHRASES_PER_FACTION = 5


@define
class Faction:
    name: str = field(default="")
    element: str = field(default="")
    mantra: str = field(init=False, default="")
    sub_cipher_translation_table: TranslationTableStrKey = field(init=False)
    phrases: list[str] = field(init=False)
    sub_cipher_translated_phrases: list[str] = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.sub_cipher_translation_table = ciphers.translation_table_make_str_keys(
            ciphers.make_substitution_cipher_translation_table()
        )  # Mongo can't handle int keys.
        self.phrases = phrases.get_random_phrases(n=NUM_PHRASES_PER_FACTION)
        self.mantra = mantras.generate_mantra()
        self.sub_cipher_translated_phrases = [
            self.translate_text_sub_cipher(phrase) for phrase in self.phrases
        ]

    def translate_text_sub_cipher(self, text: str) -> str:
        """Translates text with a substitution cipher."""
        # De-string-ify the integer keys.
        translation_table: TranslationTable = {
            ord(k): v for k, v in self.sub_cipher_translation_table.items()
        }
        return ciphers.apply_substitution_cipher(
            text, translation_table=translation_table
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "element": self.element,
            "mantra": self.mantra,
            "sub_cipher_translation_table": self.sub_cipher_translation_table,
            "phrases": self.phrases,
            "sub_cipher_translated_phrases": self.sub_cipher_translated_phrases,
        }
