from glassdolls.utils.db_clients import MongoDB, PostgresDB
from glassdolls.puzzle_generation import basic_math, ciphers, phrases, spells


def populate_spell_table(pg: PostgresDB, spell_mapping: spells.SpellChantList) -> None:
    for spell, syllables in spell_mapping.items():
        pg.insert_values(
            table="spells", cols=("spell", "syllables"), values=(spell, syllables)
        )


def populate_phrases_table(mongodb: MongoDB, phrase_list: list[str]) -> None:
    payload = []
    for phrase in phrase_list:
        # Substitution Cipher
        ciphertext, translation_table = ciphers.substitution_cipher(text=phrase)

        # Mongo requires string keys, normal transtables are
        # of the form {65: "Z", ...} for chr(65) = "A", etc.
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

    mongodb.insert_values(collection="phrases", values=payload)


# if __name__ == "__main__":
#     # pg = PostgresDB(db="glassdolls")
#     # spell_mapping: spells.SpellChantList = spells.generate_spells(
#     #     syllables_list=spells.generate_random_syllables(), spell_list=spells.SPELL_LIST
#     # )
#     # populate_spell_table(pg=pg, spell_mapping=spell_mapping)

#     mongodb = MongoDB(db="glassdolls")
#     phrase_list = phrases.get_phrase_list()
#     populate_phrases_table(mongodb=mongodb, phrase_list=phrase_list)
