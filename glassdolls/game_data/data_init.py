import random
from typing import Any

from attrs import define, field

from glassdolls.backend.db_clients import MongoDB
from glassdolls.game_data.factions import Faction
from glassdolls.pubsub.producer import Producer


@define
class Initializer:

    mongodb: MongoDB = field(default=MongoDB(), repr=False)
    producer: Producer = field(default=Producer(), repr=False)
    factions: list[Faction] = field(init=False)

    def _create_factions(self) -> list[Faction]:
        return [
            Faction(name="Hemlock", element="Dark"),
            Faction(name="Dawnstar", element="Light"),
            Faction(name="Sunfall", element="Ice"),
            Faction(name="Galeweaver", element="Wind"),
        ]

    def _populate_faction_collection(self) -> None:
        """Populate Mongo ``faction`` collection."""
        for faction in self.factions:
            self.mongodb.insert_values(
                collection="factions", values=faction.to_mongo_format()
            )

    def _create_queues_for_pubsub(self) -> None:
        try:
            # Delete and re-init the queues.
            self.producer.channel.queue_delete(queue="game.queue")
        except ValueError as e:
            pass

    # def _create_puzzles(self) -> tuple[Any, Any, Any]:
    #     # TODO: Make this nicer.
    #     faction_data = self._get_random_faction_data_from_mongo()
    #     import random

    #     return (
    #         faction_data["name"],
    #         faction_data["sub_cipher_translated_phrases"][random.randint(0, 4)],
    #         faction_data["phrases"][random.randint(0, 4)],
    #     )

    def initialize(self) -> None:
        """Main run command."""
        # TODO: We need to make this idempotent.
        self.mongodb.connect()
        self.factions = self._create_factions()
        self._populate_faction_collection()
        self._create_queues_for_pubsub()

    # def populate_spell_table(self, spell_mapping: MantraChantList) -> None:
    #     for spell, syllables in spell_mapping.items():
    #         self.pg.insert_values(
    #             table="spells", cols=("spell", "syllables"), values=(spell, syllables)
    #         )

    # def populate_phrases_table(self, phrase_list: list[str]) -> None:
    #     payload = []
    #     for phrase in phrase_list:
    #         # Casaer Cipher
    #         cesaer_shift_amount = random.randint(1, 25)
    #         cesaer_ciphertext = ciphers.cesaer_cipher(
    #             text=phrase, shift_amount=cesaer_shift_amount
    #         )

    #         # Substitution Cipher
    #         substitution_ciphertext, substitution_translation_table = (
    #             ciphers.substitution_cipher(text=phrase)
    #         )

    #         # Mongo requires string keys, normal trans-tables are
    #         # of the form {65: "Z", ...} for chr(65) = "A", etc.
    #         substitution_translation_table_str_keys = (
    #             ciphers.translation_table_make_str_keys(
    #                 translation_table=substitution_translation_table
    #             )
    #         )
    #         payload.append(
    #             {
    #                 "phrase": phrase,
    #                 "substitution": {
    #                     "ciphertext": substitution_ciphertext,
    #                     "translation_table": substitution_translation_table_str_keys,
    #                 },
    #                 "cesaer": {
    #                     "ciphertext": cesaer_ciphertext,
    #                     "shift_amount": cesaer_shift_amount,
    #                 },
    #             }
    #         )

    #     self.mongodb.insert_values(collection="phrases", values=payload)

    # def populate_puzzles(self, num: int = 10) -> None:
    #     """Populate `puzzles` table in PGDB."""
    #     self.pg.query("")

    # def initialize_all(self) -> None:
    #     """Initialize all dbs."""
    #     # Spells
    #     spell_mapping: MantraChantList = spells.generate_spells(
    #         syllables_list=spells.generate_random_syllables(),
    #         spell_list=spells.SPELL_LIST,
    #     )
    #     self.populate_spell_table(spell_mapping=spell_mapping)

    #     # Phrases
    #     phrase_list = phrases.get_phrase_list()
    #     self.populate_phrases_table(phrase_list=phrase_list)


# if __name__ == "__main__":
#     initializer = Initializer(mongodb=MongoDB())
#     initializer.initialize()
