from unittest.mock import MagicMock, patch

import pytest
from blessed.keyboard import Keystroke

from glassdolls.io.player import PlayerState
from glassdolls.io.utils import Loc


def test_player_state_initializes() -> None:
    player_state = PlayerState(health=20, magic=21, strength=22, intelligence=23)


@patch("glassdolls.io.signals.logger")
def test_player_state_handle_player_movement_runs(mock_logger: MagicMock) -> None:
    player_state = PlayerState(health=20, magic=21, strength=22, intelligence=23)
    player_state.handle_signal_player_movement(
        "test", data={"direction": Loc(x=0, y=1)}
    )

    with pytest.raises(ValueError):
        player_state.handle_signal_player_movement("test", data=None)

    with pytest.raises(ValueError):
        player_state.handle_signal_player_movement("test", data={"not_direction": 1})
