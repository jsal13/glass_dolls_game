import pytest

from glassdolls.state.map import MapState
from glassdolls.constants import MAP_TOWN_TEST_FILE


def test_map_mapstate_initializes() -> None:
    MapState()
