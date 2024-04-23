import pytest

from glassdolls.puzzles.basic_math import (add_n_numbers, generate_boss_prime,
                                           generate_composite_int,
                                           generate_large_prime)


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


def test_generate_large_prime() -> None:
    assert generate_large_prime() == 1837038795022647998


def test_generate_boss_prime() -> None:
    assert (
        generate_boss_prime()
        == 35419113627142506726261798347189877810183564435847809778757962002559750401967623860117896672946762526596452619719319240677785600
    )
