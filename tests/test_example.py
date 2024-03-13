import pytest

from glassdolls.example import example_generator


@pytest.fixture()
def example_list() -> list[int]:
    return [0, 1, 2, 3, 4]


def test_example_generator(example_list):
    assert list(example_generator(5)) == example_list
