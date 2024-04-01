import pytest
from unittest.mock import MagicMock, patch

from glassdolls.main_game import Game


@patch("glassdolls.game.signal")
def test_game_initializes(mock_signal: MagicMock) -> None:
    game = Game(
        term=MagicMock(),
        game_screen=MagicMock(),
        user_input=MagicMock(),
        player=MagicMock(),
    )
