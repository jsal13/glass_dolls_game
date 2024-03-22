import numpy as np


PRIMES = np.fromfile("data/primes.csv", dtype=int, sep=" ")


def add_n_numbers(n: int) -> tuple[list[int], int]:
    """
    Add ``n`` integers together.

    Args:
        n (int): Number of integers.

    Returns:
        tuple[list[int], int]: Returns (list of integers, sum).
    """

    int_list = np.random.randint(low=1000, high=10000, size=n).tolist()
    return (int_list, sum(int_list))


def generate_composite_int(use_primes_less_than: int = 100) -> tuple[int, list[int]]:
    """
    Generates a composite number and keeps track of prime factors.

    All prime factors are of degree 1.

    Args:
        use_primes_less_than (int): Only primes less than this value are considered.  Default 100.


    Returns:
        tuple[int, list[int]]: Returns (composite, list_of_primes).
    """

    num_primes = np.random.randint(5, 15, size=1)[0]
    primes = np.random.choice(
        PRIMES[PRIMES < use_primes_less_than], size=num_primes
    ).astype(int)

    return (np.prod(primes), primes.tolist())


print(generate_composite_int())
