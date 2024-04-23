import pytest

from glassdolls.constants import MAP_TOWN_TEST_FILE
from glassdolls.state.map import MapState


def test_map_mapstate_initializes() -> None:
    MapState.create_mapstate()
