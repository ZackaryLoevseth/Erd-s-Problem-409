#!/usr/bin/env python3
"""Independent factor-from-scratch verification of the F=71 orbit."""
from __future__ import annotations

import math

START = 6_668_696_999
EXPECTED_STEPS = 71
EXPECTED_TERMINAL = 9_500_401


def factorint_trial(n: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    p = 3
    while p * p <= n:
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
        p += 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    factors = factorint_trial(n)
    return len(factors) == 1 and next(iter(factors.items())) == (n, 1)


def phi_from_factors(factors: dict[int, int]) -> int:
    result = 1
    for p, e in factors.items():
        result *= (p - 1) * p ** (e - 1)
    return result


def main() -> None:
    n = START
    steps = 0
    checkpoints = {
        0: 6_668_696_999,
        1: 6_665_198_137,
        2: 6_152_490_577,
        3: 6_148_888_817,
    }
    while not is_prime_trial(n):
        if steps in checkpoints and n != checkpoints[steps]:
            raise AssertionError(f"checkpoint mismatch at step {steps}: {n}")
        factors = factorint_trial(n)
        n = phi_from_factors(factors) + 1
        steps += 1
        if steps > EXPECTED_STEPS:
            raise AssertionError("trajectory exceeded expected length")

    if (steps, n) != (EXPECTED_STEPS, EXPECTED_TERMINAL):
        raise AssertionError(
            f"expected ({EXPECTED_STEPS}, {EXPECTED_TERMINAL}), got ({steps}, {n})"
        )
    print(steps, n)


if __name__ == "__main__":
    main()
