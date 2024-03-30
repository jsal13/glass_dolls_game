# See: https://docs.pytest.org/en/7.1.x/reference/fixtures.html
from typing import Any, Generator

import numpy as np
import pytest


@pytest.fixture(autouse=True, scope="function")
def set_np_seed() -> Generator[Any, Any, Any]:
    """Fixture to execute asserts before and after a test is run"""
    np.random.seed(seed=1234)
    yield
