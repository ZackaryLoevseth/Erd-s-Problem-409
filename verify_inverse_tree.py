#!/usr/bin/env python3
"""Independent exact verifier for the rooted inverse-totient tree.

This implementation uses divisor generation plus dynamic programming over exact
Euler-phi contributions. It does not import SymPy and is intentionally separate
from the recursive generator used to create the published data.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TREE_PATH = ROOT / "data" / "inverse_totient_tree.json.gz"


def is_prime_64(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    # Deterministic for unsigned 64-bit integers.
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        a %= n
        if a in (0, 1):
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def factorint_trial(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("factorization requires n >= 1")
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


def divisors(factors: dict[int, int]) -> list[int]:
    values = [1]
    for p, e in sorted(factors.items()):
        powers = [p**k for k in range(e + 1)]
        values = [a * b for a in values for b in powers]
    return sorted(values)


def phi_from_factorization(factors: dict[int, int]) -> int:
    value = 1
    for p, e in factors.items():
        value *= (p - 1) * p ** (e - 1)
    return value


def inverse_totients_dp(m: int) -> list[int]:
    """Return every n with phi(n)=m by exact prime-power contribution DP."""
    m_factors = factorint_trial(m)
    options: dict[int, list[tuple[int, int]]] = {}
    for d in divisors(m_factors):
        p = d + 1
        if not is_prime_64(p):
            continue
        group: list[tuple[int, int]] = []
        power = p
        contribution = d
        while m % contribution == 0:
            group.append((power, contribution))
            power *= p
            contribution *= p
        options[p] = group

    # contribution product -> possible n products after processing each prime.
    dp: dict[int, set[int]] = {1: {1}}
    for p in sorted(options):
        updated: dict[int, set[int]] = {k: set(v) for k, v in dp.items()}
        for used_contribution, partial_ns in dp.items():
            for power, contribution in options[p]:
                new_contribution = used_contribution * contribution
                if m % new_contribution:
                    continue
                bucket = updated.setdefault(new_contribution, set())
                for partial_n in partial_ns:
                    bucket.add(partial_n * power)
        dp = updated

    values = sorted(dp.get(m, set()))
    for n in values:
        if phi_from_factorization(factorint_trial(n)) != m:
            raise AssertionError(f"internal DP error: phi({n}) != {m}")
    return values


def main() -> None:
    with gzip.open(TREE_PATH, "rt", encoding="utf-8") as handle:
        tree = json.load(handle)

    if tree.get("schema") != "erdos409-inverse-totient-tree-v1":
        raise AssertionError("unexpected inverse-tree schema")

    levels = {int(item["F"]): [int(x) for x in item["values"]] for item in tree["levels"]}
    expected_edges = {
        (int(edge["F"]), int(edge["child"]), int(edge["parent"]))
        for edge in tree["edges"]
    }

    if levels.get(68) != [6_148_888_817]:
        raise AssertionError("unexpected rooted F=68 level")

    actual_edges: set[tuple[int, int, int]] = set()
    for f in (69, 70, 71, 72):
        found: set[int] = set()
        for parent in levels[f - 1]:
            children = inverse_totients_dp(parent - 1)
            for child in children:
                found.add(child)
                actual_edges.add((f, child, parent))
        if sorted(found) != levels[f]:
            raise AssertionError(
                f"level F={f} mismatch: stored {len(levels[f])}, recomputed {len(found)}"
            )

    if actual_edges != expected_edges:
        missing = sorted(expected_edges - actual_edges)[:5]
        extra = sorted(actual_edges - expected_edges)[:5]
        raise AssertionError(f"edge mismatch; missing={missing}, extra={extra}")

    counts = {f: len(levels[f]) for f in sorted(levels)}
    expected_counts = {68: 1, 69: 10, 70: 42, 71: 10, 72: 0}
    if counts != expected_counts:
        raise AssertionError(f"unexpected level counts: {counts}")

    print(
        "VERIFIED inverse tree: "
        "F68=1, F69=10, F70=42, F71=10, F72=0; "
        f"{len(actual_edges)} exact parent-child edges."
    )


if __name__ == "__main__":
    main()
