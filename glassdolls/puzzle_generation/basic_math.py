import numpy as np

from glassdolls.constants import DATA_PRIMES_FILE_LOC

PRIMES = np.fromfile(DATA_PRIMES_FILE_LOC, dtype=int, sep=" ")
BOSS_PRIME_NUMBER = 7 + 1  # Seven levels, plus an additional prime.


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


def generate_large_prime() -> int:
    """
    Generates a "large" prime for use in crypto.

    Returns:
        int: The large prime number.
    """

    product = 0
    while product <= 0:
        num_primes_to_multiply = np.random.randint(2, 10)
        primes = np.random.choice(PRIMES, size=num_primes_to_multiply)
        product = int(np.prod(primes))

    return product + 1


def generate_boss_prime(num_primes: int = BOSS_PRIME_NUMBER) -> int:
    """Generate a very, very large prime from other large primes."""
    boss_prime = 1
    for _ in range(num_primes):
        large_prime = generate_large_prime()
        boss_prime *= large_prime
    return boss_prime
