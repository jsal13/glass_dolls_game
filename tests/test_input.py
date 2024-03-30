import string

import pytest
from blessed.keyboard import Keystroke

from glassdolls.input import UserInput


@pytest.mark.parametrize(
    "user_input",
    list("Aa1!@#$%^&*()-=_+\{\}[]|;:'\"\\,./?><"),
)
def test_user_input_parses_ascii_key_correctly(user_input: str) -> None:
    ui = UserInput(keypress=Keystroke(user_input))
    assert ui._key == user_input.upper()
