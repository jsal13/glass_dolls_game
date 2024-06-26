from unittest.mock import MagicMock, patch

import pytest
from blessed.keyboard import Keystroke

from glassdolls.io.input import UserInput


def test_user_input_initializes() -> None:
    user_input = UserInput(term=MagicMock())


# def test_user_input_handle_signal_user_input_runs() -> None:
#     user_input = UserInput(term=MagicMock())
#     user_input.handle_signal_user_input("test", data={"key": "KEY_LEFT"})

#     with pytest.raises(ValueError):
#         user_input.handle_signal_user_input("test", data=None)

#     with pytest.raises(ValueError):
#         user_input.handle_signal_user_input("test", data={"not_key": "KEY_LEFT"})


def test_user_input_wait_for_key_runs() -> None:
    mock_terminal = MagicMock()
    mock_terminal.cbreak = MagicMock()
    mock_terminal.inkey = lambda: Keystroke("A")
    user_input = UserInput(term=mock_terminal)
    user_input.wait_for_key()


def test_user_input_wait_for_key_runs_with_sequence_key() -> None:
    mock_terminal = MagicMock()
    mock_terminal.cbreak = MagicMock()
    mock_terminal.inkey = lambda: Keystroke("KEY_LEFT")
    user_input = UserInput(term=mock_terminal)
    user_input.wait_for_key()


def test_user_input_wait_for_key_quits_with_q() -> None:
    mock_terminal = MagicMock()
    mock_terminal.cbreak = MagicMock()
    mock_terminal.inkey = lambda: Keystroke("Q")
    user_input = UserInput(term=mock_terminal)
    with patch("glassdolls.io.input.sys.exit") as exit_mock:
        user_input.wait_for_key()
        assert exit_mock.called
