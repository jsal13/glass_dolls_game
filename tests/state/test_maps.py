import pytest

from glassdolls.state.maps import MapState
from glassdolls.constants import MAP_TOWN_TEST_FILE


def test_map_mapstate_initializes() -> None:
    MapState()
