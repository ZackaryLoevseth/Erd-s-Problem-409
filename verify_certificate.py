#!/usr/bin/env python3
"""Package-free verification of the complete F=71 trajectory certificate."""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRAJECTORY_PATH = ROOT / "data" / "trajectory_certificate.json.gz"
PRIME_PATH = ROOT / "data" / "prime_certificates.json.gz"

EXPECTED_START = 6_668_696_999
EXPECTED_STEPS = 71
EXPECTED_TERMINAL = 9_500_401
EXPECTED_RECORD_CHAIN = {
    68: 6_148_888_817,
    69: 6_152_490_577,
    70: 6_665_198_137,
    71: 6_668_696_999,
}


def factor_product(factors: list[list[int]]) -> int:
    value = 1
    for p, e in factors:
        if p < 2 or e < 1:
            raise AssertionError("invalid factor entry")
        value *= p**e
    return value


def phi_from_factors(factors: list[list[int]]) -> int:
    value = 1
    for p, e in factors:
        value *= (p - 1) * p ** (e - 1)
    return value


def main() -> None:
    with gzip.open(TRAJECTORY_PATH, "rt", encoding="utf-8") as handle:
        packet = json.load(handle)
    with gzip.open(PRIME_PATH, "rt", encoding="utf-8") as handle:
        prime_packet = json.load(handle)

    if packet.get("schema") != "erdos409-trajectory-certificate-v2":
        raise AssertionError("unexpected trajectory schema")
    claim = packet["claim"]
    if (
        int(claim["start"]),
        int(claim["steps"]),
        int(claim["terminal_prime"]),
    ) != (EXPECTED_START, EXPECTED_STEPS, EXPECTED_TERMINAL):
        raise AssertionError("claim header mismatch")

    certs = {int(k): v for k, v in prime_packet["certificates"].items()}
    verified_primes: set[int] = set()
    active: set[int] = set()

    def verify_prime(p: int) -> None:
        if p in verified_primes:
            return
        if p in active:
            raise AssertionError(f"prime-certificate cycle at {p}")
        cert = certs.get(p)
        if cert is None or int(cert.get("p", -1)) != p:
            raise AssertionError(f"missing prime certificate for {p}")
        active.add(p)
        if p == 2:
            if not cert.get("base"):
                raise AssertionError("invalid base certificate")
        else:
            factors = [[int(q), int(e)] for q, e in cert["p_minus_1_factorization"]]
            if factor_product(factors) != p - 1:
                raise AssertionError(f"bad factorization of {p}-1")
            for q, _ in factors:
                verify_prime(q)
            a = int(cert["witness"])
            if pow(a, p - 1, p) != 1:
                raise AssertionError(f"Fermat condition failed for {p}")
            for q, _ in factors:
                if math.gcd(pow(a, (p - 1) // q, p) - 1, p) != 1:
                    raise AssertionError(f"Lucas condition failed for p={p}, q={q}")
        active.remove(p)
        verified_primes.add(p)

    nodes = packet["nodes"]
    if len(nodes) != EXPECTED_STEPS + 1:
        raise AssertionError("wrong trajectory length")

    for i, node in enumerate(nodes):
        if int(node["index"]) != i:
            raise AssertionError(f"wrong node index at {i}")
        n = int(node["n"])
        factors = [[int(p), int(e)] for p, e in node["factorization"]]
        for p, _ in factors:
            verify_prime(p)
        if factor_product(factors) != n:
            raise AssertionError(f"factorization product mismatch at index {i}")

        if i < EXPECTED_STEPS:
            if node["status"] != "composite":
                raise AssertionError(f"nonterminal node {i} not marked composite")
            if len(factors) == 1 and factors[0][1] == 1:
                raise AssertionError(f"nonterminal node {i} is actually prime")
            phi = phi_from_factors(factors)
            nxt = int(nodes[i + 1]["n"])
            if int(node["phi"]) != phi:
                raise AssertionError(f"totient mismatch at index {i}")
            if int(node["next"]) != nxt or phi + 1 != nxt:
                raise AssertionError(f"transition mismatch at index {i}")
        else:
            if node["status"] != "prime" or n != EXPECTED_TERMINAL:
                raise AssertionError("bad terminal node")
            if node["phi"] is not None or node["next"] is not None:
                raise AssertionError("terminal node must not have a transition")

    record_chain = {int(item["F"]): int(item["witness"]) for item in packet["record_chain"]}
    if record_chain != EXPECTED_RECORD_CHAIN:
        raise AssertionError("record-chain metadata mismatch")
    for f, witness in EXPECTED_RECORD_CHAIN.items():
        index = EXPECTED_STEPS - f
        if int(nodes[index]["n"]) != witness:
            raise AssertionError(f"F={f} witness is not at the expected trajectory depth")

    print(
        "VERIFIED: F(6668696999)=71; terminal prime=9500401; "
        f"{len(nodes)} nodes; {len(verified_primes)} prime certificates used."
    )


if __name__ == "__main__":
    main()
