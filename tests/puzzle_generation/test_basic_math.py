from typing import Generator, Any
import pytest
import numpy as np

from glassdolls.puzzle_generation.basic_math import (
    add_n_numbers,
    generate_composite_int,
)


@pytest.fixture()
def test_add_values_and_sum() -> tuple[list[int], int]:
    return ([9915, 2318, 8221, 8540, 1664, 7137, 7833, 9471, 8322, 9222], 72643)


@pytest.fixture()
def test_prime_factors_and_product() -> tuple[int, list[int]]:
    return (112188973673911, [17, 79, 41, 73, 97, 53, 61, 89])


def test_add_n_numbers(test_add_values_and_sum: tuple[list[int], int]) -> None:
    int_list, summation = add_n_numbers(n=10)
    expected_int_list, expected_summation = test_add_values_and_sum
    assert int_list == expected_int_list
    assert summation == expected_summation


def test_generate_small_composite_int(
    test_prime_factors_and_product: tuple[int, list[int]]
) -> None:
    value, factors = generate_composite_int()
    expected_value, expected_factors = test_prime_factors_and_product
    assert value == expected_value
    assert factors == expected_factors
