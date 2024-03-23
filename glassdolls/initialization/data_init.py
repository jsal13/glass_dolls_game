from typing import Any

from glassdolls.utils.db_clients import MongoDB, PostgresDB
from glassdolls.puzzle_generation import basic_math, ciphers, phrases, spells


def populate_spell_table(spell_mapping: spells.SpellChantList) -> None:
    pg = PostgresDB(db="glassdolls")
    for spell, syllables in spell_mapping.items():
        pg.insert_values(
            table="spells", cols=("spell", "syllables"), values=(spell, syllables)
        )


def populate_phrases_table(payload: list[dict["str", Any]]) -> None:
    mongodb = MongoDB(db="glassdolls")
    mongodb.insert_values(collection="phrases", values=payload)


if __name__ == "__main__":
    # spell_mapping = spells.generate_spells(
    #     syllables_list=spells.generate_random_syllables(), spell_list=spells.SPELL_LIST
    # )
    # populate_spell_table(spell_mapping=spell_mapping)

    phrase_list = phrases.get_phrase_list()
    payload = []
    for phrase in phrase_list:
        ciphertext, translation_table = ciphers.substitution_cipher(text=phrase)

        # Mongo requires string keys.
        translation_table_str_keys = ciphers.translation_table_make_str_keys(
            translation_table=translation_table
        )
        payload.append(
            {
                "phrase": phrase,
                "substitution_ciphertext": ciphertext,
                "substitution_translation_table": translation_table_str_keys,
            }
        )
    populate_phrases_table(payload=payload)
