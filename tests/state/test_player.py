import pytest

from glassdolls.state.player import PlayerState


def test_map_playerstate_initializes() -> None:
    PlayerState.create_default_playerstate()
