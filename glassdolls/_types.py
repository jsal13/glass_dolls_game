from typing import TypeAlias

# Maps
MapTiles: TypeAlias = list[list[str]]

# Ciphers
TranslationTable: TypeAlias = dict[int, str]
TranslationTableStrKey: TypeAlias = dict[str, str]

# Spells
SyllableList: TypeAlias = list[str]
SpellChantList: TypeAlias = dict[str, str]
