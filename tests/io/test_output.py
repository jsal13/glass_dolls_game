import pytest
from unittest.mock import MagicMock, patch


from glassdolls.io.output import (
    Window,
    InputWindow,
    MapDisplay,
    GameText,
    DescriptionDisplay,
    GameScreen,
)

from glassdolls.utils import Loc


def test_map_display_initializes() -> None:
    map_display = MapDisplay()


def test_description_display_initializes() -> None:
    description_display = DescriptionDisplay()
    description_display.title = "test"
    description_display.text = "test text!"


@patch("glassdolls.io.output.DescriptionDisplay.print_at")
def test_description_display_display_runs(mock_printer: MagicMock) -> None:
    description_display = DescriptionDisplay()
    description_display.title = "test"
    description_display.text = "test text!"

    description_display.display()


def test_game_screen_initializes() -> None:
    game_screen = GameScreen(term=MagicMock())
