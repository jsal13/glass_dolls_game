import pytest
from unittest.mock import MagicMock
from blessed.keyboard import Keystroke

from glassdolls.io.input import UserInput


# @pytest.mark.parametrize(
#     "user_input",
#     list("Aa1!@#$%^&*()-=_+\{\}[]|;:'\"\\,./?><"),
# )


def test_user_input_initializes() -> None:
    user_input = UserInput(term=MagicMock())


def test_user_input_handle_signal_user_input_runs() -> None:
    user_input = UserInput(term=MagicMock())
    user_input.handle_signal_user_input("test", data={"key": "KEY_LEFT"})

    with pytest.raises(ValueError):
        user_input.handle_signal_user_input("test", data=None)
        user_input.handle_signal_user_input("test", data={"not_key": "KEY_LEFT"})
