# See: https://docs.pytest.org/en/7.1.x/reference/fixtures.html
from typing import Generator, Any
import pytest
import numpy as np


@pytest.fixture(autouse=True, scope="function")
def set_np_seed() -> Generator[Any, Any, Any]:
    """Fixture to execute asserts before and after a test is run"""
    np.random.seed(seed=1234)
    yield
