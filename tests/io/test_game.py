import pytest
from unittest.mock import MagicMock, patch

from glassdolls.io.game import Game


@patch("glassdolls.io.game.signal")
def test_game_initializes(mock_signal: MagicMock) -> None:
    game = Game(
        term=MagicMock(),
        game_screen=MagicMock(),
        user_input=MagicMock(),
        player=MagicMock(),
    )
