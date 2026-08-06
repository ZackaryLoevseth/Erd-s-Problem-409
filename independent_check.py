#!/usr/bin/env python3
"""Independent dependency-free recomputation of the F=68 witness.

Unlike verify_certificate.py, this script does not read the stored
factorizations. It factors every trajectory node from scratch by trial
division, recomputes Euler's totient, and checks the terminal prime.
"""

from __future__ import annotations

from math import isqrt

START = 6_148_888_817
EXPECTED_STEPS = 68
EXPECTED_TERMINAL = 9_500_401


def factorize(n: int) -> dict[int, int]:
    if n < 2:
        raise ValueError("factorize expects n >= 2")

    factors: dict[int, int] = {}
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2

    d = 3
    while d <= isqrt(n):
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 2

    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    factors = factorize(n)
    return factors == {n: 1}


def phi_from_factors(factors: dict[int, int]) -> int:
    result = 1
    for p, exponent in factors.items():
        result *= (p - 1) * p ** (exponent - 1)
    return result


def main() -> None:
    n = START
    steps = 0

    while not is_prime(n):
        factors = factorize(n)
        n = phi_from_factors(factors) + 1
        steps += 1

    print(steps, n)
    if (steps, n) != (EXPECTED_STEPS, EXPECTED_TERMINAL):
        raise RuntimeError(
            "Unexpected result: "
            f"expected ({EXPECTED_STEPS}, {EXPECTED_TERMINAL}), got ({steps}, {n})"
        )


if __name__ == "__main__":
    main()
