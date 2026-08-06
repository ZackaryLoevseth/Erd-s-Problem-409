#!/usr/bin/env python3
"""Verify every recursive Lucas/Pratt-style prime certificate."""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CERT_PATH = ROOT / "data" / "prime_certificates.json.gz"


def product_factorization(factors: list[list[int]]) -> int:
    value = 1
    for p, e in factors:
        if p < 2 or e < 1:
            raise AssertionError("invalid factor entry")
        value *= p**e
    return value


def main() -> None:
    with gzip.open(CERT_PATH, "rt", encoding="utf-8") as handle:
        packet = json.load(handle)
    if packet.get("schema") != "lucas-pratt-prime-certificates-v2":
        raise AssertionError("unexpected prime-certificate schema")
    certs = {int(k): v for k, v in packet["certificates"].items()}
    verified: set[int] = set()
    active: set[int] = set()

    def verify_prime(p: int) -> None:
        if p in verified:
            return
        if p in active:
            raise AssertionError(f"cycle in prime certificates at {p}")
        cert = certs.get(p)
        if cert is None or int(cert.get("p", -1)) != p:
            raise AssertionError(f"missing certificate for {p}")
        active.add(p)
        if p == 2:
            if not cert.get("base"):
                raise AssertionError("2 must be the base certificate")
        else:
            factors = [[int(q), int(e)] for q, e in cert["p_minus_1_factorization"]]
            if product_factorization(factors) != p - 1:
                raise AssertionError(f"bad factorization of {p}-1")
            for q, _ in factors:
                verify_prime(q)
            a = int(cert["witness"])
            if not 1 < a < p:
                raise AssertionError(f"invalid witness range for {p}")
            if pow(a, p - 1, p) != 1:
                raise AssertionError(f"Fermat condition failed for {p}")
            for q, _ in factors:
                if math.gcd(pow(a, (p - 1) // q, p) - 1, p) != 1:
                    raise AssertionError(f"Lucas condition failed for p={p}, q={q}")
        active.remove(p)
        verified.add(p)

    for p in sorted(certs):
        verify_prime(p)
    if verified != set(certs):
        raise AssertionError("not all prime certificates were reached")
    print(f"VERIFIED: {len(verified)} recursive prime certificates.")


if __name__ == "__main__":
    main()
