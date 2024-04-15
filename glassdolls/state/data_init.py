import random

from glassdolls._types import SpellChantList
from glassdolls.puzzle_generation import basic_math, ciphers, phrases, spells
from glassdolls.utils.db_clients import MongoDB, PostgresDB


class Initializer:

    def __init__(self, pg: PostgresDB, mongodb: MongoDB) -> None:
        self.pg = pg
        self.mongodb = mongodb

        # Connect to the dbs.
        self.pg.connect()
        self.mongodb.connect()

    def populate_spell_table(self, spell_mapping: SpellChantList) -> None:
        for spell, syllables in spell_mapping.items():
            self.pg.insert_values(
                table="spells", cols=("spell", "syllables"), values=(spell, syllables)
            )

    def populate_phrases_table(self, phrase_list: list[str]) -> None:
        payload = []
        for phrase in phrase_list:
            # Casaer Cipher
            cesaer_shift_amount = random.randint(1, 25)
            cesaer_ciphertext = ciphers.cesaer_cipher(
                text=phrase, shift_amount=cesaer_shift_amount
            )

            # Substitution Cipher
            substitution_ciphertext, substitution_translation_table = (
                ciphers.substitution_cipher(text=phrase)
            )

            # Mongo requires string keys, normal trans-tables are
            # of the form {65: "Z", ...} for chr(65) = "A", etc.
            substitution_translation_table_str_keys = (
                ciphers.translation_table_make_str_keys(
                    translation_table=substitution_translation_table
                )
            )
            payload.append(
                {
                    "phrase": phrase,
                    "substitution": {
                        "ciphertext": substitution_ciphertext,
                        "translation_table": substitution_translation_table_str_keys,
                    },
                    "cesaer": {
                        "ciphertext": cesaer_ciphertext,
                        "shift_amount": cesaer_shift_amount,
                    },
                }
            )

        self.mongodb.insert_values(collection="phrases", values=payload)

    def initialize_all(self) -> None:
        """Initialize all dbs."""
        # Spells
        spell_mapping: SpellChantList = spells.generate_spells(
            syllables_list=spells.generate_random_syllables(),
            spell_list=spells.SPELL_LIST,
        )
        self.populate_spell_table(spell_mapping=spell_mapping)

        # Phrases
        phrase_list = phrases.get_phrase_list()
        self.populate_phrases_table(phrase_list=phrase_list)


if __name__ == "__main__":
    initializer = Initializer(pg=PostgresDB(), mongodb=MongoDB())
    initializer.initialize_all()
