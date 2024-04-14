import pytest
from unittest.mock import MagicMock, patch

from glassdolls.io.output import (
    MapDisplay,
    LineDisplay,
    OptionsDisplay,
    DescriptionDisplay,
    GameScreen,
    TerminalPrinter,
)
from glassdolls.io.utils import Loc


def test_terminal_printer_print_at_errors_out_for_fake_color() -> None:
    tp = TerminalPrinter(term=MagicMock())
    with pytest.raises(ValueError):
        tp.print_at(x=1, y=1, text="test", color="fake_color")


def test_map_display_initializes() -> None:
    map_display = MapDisplay(
        term=MagicMock(),
        map_ascii=[["." for _ in range(10)] for _ in range(10)],
        x_map_start=0,
        y_map_start=1,
    )


def test_line_display_initializes() -> None:
    line_display = LineDisplay(
        term=MagicMock(),
    )


def test_options_display_initializes() -> None:
    options_display = OptionsDisplay(term=MagicMock(), options=["hi", "howdy"])


def test_options_display_gets_and_sets_correctly() -> None:
    options_display = OptionsDisplay(term=MagicMock(), options=["hi", "howdy"])

    options_display.options = ["test", "taste"]


def test_description_display_initializes() -> None:
    description_display = DescriptionDisplay(
        term=MagicMock(), title="test", text="test text!"
    )


def test_description_display_gets_and_sets_correctly() -> None:
    description_display = DescriptionDisplay(
        term=MagicMock(), title="test", text="test text!"
    )
    description_display.title = "new title"
    description_display.text = "new text"


@patch("glassdolls.io.output.DescriptionDisplay.print_at")
def test_description_display_display_runs(mock_printer: MagicMock) -> None:
    description_display = DescriptionDisplay(
        term=MagicMock(), title="test", text="test text!"
    )
    description_display.display(x=1, y=2)


def test_game_screen_initializes() -> None:
    game_screen = GameScreen(term=MagicMock())


def test_game_screen_refresh_screen_runs() -> None:
    game_screen = GameScreen(term=MagicMock())
    game_screen._refresh_screen()


def test_game_screen_refresh_display_runs() -> None:
    game_screen = GameScreen(term=MagicMock())
    game_screen.refresh_display()


def test_game_screen_handle_player_loc_updated_runs() -> None:
    game_screen = GameScreen(term=MagicMock())
    game_screen.handle_player_loc_updated("test", data={"location": Loc(x=0, y=1)})


@patch("glassdolls.io.signals.logger")
def test_game_screen_handle_display_updates_runs(mock_logger: MagicMock) -> None:
    game_screen = GameScreen(term=MagicMock())
    game_screen.handle_display_updates("test", data={"location": Loc(x=0, y=1)})
