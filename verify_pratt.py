#!/usr/bin/env python3
"""Verify every recursive prime certificate in data/prime_certificates.json."""

from __future__ import annotations

import gzip
import json
import math
from pathlib import Path
from typing import Any

PATH = Path(__file__).resolve().parent / "data" / "prime_certificates.json.gz"


def verify_prime(
    p: int,
    certs: dict[str, dict[str, Any]],
    verified: set[int],
    active: set[int],
) -> None:
    if p in verified:
        return
    if p in active:
        raise RuntimeError(f"Dependency cycle at {p}")
    active.add(p)

    cert = certs.get(str(p))
    if cert is None or cert.get("n") != p:
        raise RuntimeError(f"Missing or mismatched certificate for {p}")

    if p == 2:
        if cert.get("base_case") is not True:
            raise RuntimeError("Invalid certificate for 2")
    else:
        factors = cert.get("p_minus_1_factorization")
        if not isinstance(factors, list) or not factors:
            raise RuntimeError(f"Missing p-1 factorization for {p}")

        product = 1
        distinct: list[int] = []
        for q, exponent in factors:
            verify_prime(q, certs, verified, active)
            product *= q**exponent
            distinct.append(q)

        if product != p - 1:
            raise RuntimeError(f"Incorrect p-1 factorization for {p}")

        a = cert.get("witness")
        if not isinstance(a, int) or not (1 < a < p):
            raise RuntimeError(f"Invalid witness for {p}")
        if pow(a, p - 1, p) != 1:
            raise RuntimeError(f"Fermat condition failed for {p}")
        for q in distinct:
            if math.gcd(pow(a, (p - 1) // q, p) - 1, p) != 1:
                raise RuntimeError(f"Lucas condition failed for p={p}, q={q}")

    active.remove(p)
    verified.add(p)


def main() -> None:
    with gzip.open(PATH, "rt", encoding="utf-8") as handle:
        data = json.load(handle)
    certs = data["certificates"]
    verified: set[int] = set()

    for key in sorted(certs, key=int):
        verify_prime(int(key), certs, verified, set())

    if len(verified) != data["certificate_count"]:
        raise RuntimeError("Certificate-count mismatch")

    print(f"VERIFIED: {len(verified)} recursive prime certificates.")


if __name__ == "__main__":
    main()
