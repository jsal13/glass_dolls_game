import pytest
from unittest.mock import MagicMock
from blessed.keyboard import Keystroke

from glassdolls.io.utils import Loc


def test_loc_initializes() -> None:
    loc = Loc(x=1, y=2)
    assert loc.x == 1
    assert loc.y == 2


@pytest.mark.parametrize("x1", [-1, 0, 1])
@pytest.mark.parametrize("x2", [-1, 0, 1])
@pytest.mark.parametrize("y1", [-1, 0, 1])
@pytest.mark.parametrize("y2", [-1, 0, 1])
def test_loc_adds_correctly(x1: int, x2: int, y1: int, y2: int) -> None:
    assert Loc(x1, y1) + Loc(x2, y2) == Loc(x1 + x2, y1 + y2)
    assert (Loc(x1, y1) + Loc(x2, y2)).x == x1 + x2
    assert (Loc(x1, y1) + Loc(x2, y2)).y == y1 + y2


def test_loc_astuple_returns_correctly() -> None:
    loc_tuple = Loc(x=1, y=2).astuple()
    assert type(loc_tuple) == tuple
    assert loc_tuple == (1, 2)
