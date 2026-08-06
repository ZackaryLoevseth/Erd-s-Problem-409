#!/usr/bin/env python3
"""Minimal SymPy verification of the Erdős Problem #409 F=68 witness."""

from sympy import isprime, totient

START = 6_148_888_817
EXPECTED_STEPS = 68
EXPECTED_TERMINAL = 9_500_401


def main() -> None:
    n = START
    steps = 0

    while not isprime(n):
        n = int(totient(n)) + 1
        steps += 1

    print(steps, n)

    if (steps, n) != (EXPECTED_STEPS, EXPECTED_TERMINAL):
        raise RuntimeError(
            "Unexpected result: "
            f"expected ({EXPECTED_STEPS}, {EXPECTED_TERMINAL}), got ({steps}, {n})"
        )


if __name__ == "__main__":
    main()
