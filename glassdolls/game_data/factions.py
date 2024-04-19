import hashlib
from typing import Any

from attrs import define, field

from glassdolls._types import TranslationTable, TranslationTableStrKey
from glassdolls.puzzles import basic_math, ciphers, mantras, phrases

NUM_PHRASES_PER_FACTION = 5


@define
class Faction:
    name: str = field(default="")
    element: str = field(default="")
    mantra: str = field(init=False, default="")
    sub_cipher_translation_table: TranslationTableStrKey = field(init=False)
    phrases: list[dict[str, Any]] = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.sub_cipher_translation_table = ciphers.translation_table_make_str_keys(
            ciphers.make_substitution_cipher_translation_table()
        )  # Mongo can't handle int keys.
        self.mantra = mantras.generate_mantra()
        _phrases = phrases.get_random_phrases(n=NUM_PHRASES_PER_FACTION)

        # The "code" here is not meant to be secure, just a hash of a small size that makes a reasonable "user copy-paste" code to represent this particular phrase.  Used for mongo fetching.
        self.phrases = []
        for _phrase in _phrases:

            # Creates solution, adds it to the phrase.
            solution = mantras.generate_mantra()
            solution_sent = f"\nTHE CODE IS {solution}"
            phrase = _phrase + solution_sent

            self.phrases.append(
                {
                    "code": hashlib.blake2s(
                        phrase.encode("utf-8"),
                        digest_size=8,
                    ).hexdigest(),
                    "phrase": phrase,
                    "sub_cipher": self._translate_text_sub_cipher(phrase),
                    "solution": solution,
                    "solution_hash": hashlib.blake2s(
                        solution.encode("utf-8"),
                        digest_size=20,
                    ).hexdigest(),
                }
            )

    def _translate_text_sub_cipher(self, text: str) -> str:
        """Translates text with a substitution cipher."""
        # De-string-ify the integer keys.
        translation_table: TranslationTable = {
            ord(k): v for k, v in self.sub_cipher_translation_table.items()
        }
        return ciphers.apply_substitution_cipher(
            text, translation_table=translation_table
        )

    def to_mongo_format(self) -> list[dict[str, Any]]:
        return [
            {
                "name": self.name,
                "element": self.element,
                "mantra": self.mantra,
                "phrases": phrase,
            }
            for phrase in self.phrases
        ]
