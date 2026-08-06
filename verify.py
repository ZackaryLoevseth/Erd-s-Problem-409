#!/usr/bin/env python3
"""Minimal SymPy verification of the F=71 witness."""
from __future__ import annotations

from sympy import isprime, totient

START = 6_668_696_999
EXPECTED = (71, 9_500_401)


def main() -> None:
    n = START
    steps = 0
    while not isprime(n):
        n = int(totient(n)) + 1
        steps += 1
    print(steps, n)
    if (steps, n) != EXPECTED:
        raise RuntimeError(f"expected {EXPECTED}, got {(steps, n)}")


if __name__ == "__main__":
    main()
