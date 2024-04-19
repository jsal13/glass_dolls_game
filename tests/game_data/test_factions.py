import pytest

from glassdolls.game_data.factions import Faction


def test_map_faction_initializes() -> None:
    Faction(name="Test", element="Test")
