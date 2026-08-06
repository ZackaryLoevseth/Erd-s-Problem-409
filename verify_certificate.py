#!/usr/bin/env python3
"""Verify the full Erdős Problem #409 trajectory certificate using Python only.

This checker does not call SymPy. It validates:
  * recursive Lucas/Pratt-style primality certificates for all prime factors;
  * every stated factorization;
  * every Euler-totient computation;
  * every transition n -> phi(n) + 1;
  * the exact 68-step stopping condition and terminal prime.
"""

from __future__ import annotations

import gzip
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
TRAJECTORY_CERT = ROOT / "data" / "certificate.json.gz"
PRIME_CERTS = ROOT / "data" / "prime_certificates.json.gz"

EXPECTED_START = 6_148_888_817
EXPECTED_STEPS = 68
EXPECTED_TERMINAL = 9_500_401


class VerificationError(RuntimeError):
    """Raised when a certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        if path.suffix == ".gz":
            with gzip.open(path, "rt", encoding="utf-8") as handle:
                return json.load(handle)
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VerificationError(f"Could not load {path}: {exc}") from exc


def verify_prime(
    p: int,
    certificates: dict[str, dict[str, Any]],
    memo: set[int],
    active: set[int],
) -> None:
    """Verify p using a recursive Lucas/Pratt-style certificate.

    For p > 2, the certificate gives the complete prime factorization of p-1
    and a witness a satisfying:
        a^(p-1) == 1 (mod p)
    and, for every prime q dividing p-1,
        gcd(a^((p-1)/q) - 1, p) == 1.

    These conditions imply that the multiplicative order of a modulo every
    prime divisor of p is p-1, forcing p itself to be prime.
    """
    if p in memo:
        return
    require(p not in active, f"Cycle in prime-certificate dependency at {p}")
    active.add(p)

    cert = certificates.get(str(p))
    require(cert is not None, f"Missing prime certificate for {p}")
    require(cert.get("n") == p, f"Prime certificate key/value mismatch for {p}")

    if p == 2:
        require(cert.get("base_case") is True, "Invalid base certificate for 2")
        memo.add(2)
        active.remove(2)
        return

    require(p > 2 and p % 2 == 1, f"Non-base prime candidate must be odd: {p}")
    require(cert.get("base_case") is False, f"Invalid non-base marker for {p}")

    factorization = cert.get("p_minus_1_factorization")
    require(isinstance(factorization, list) and factorization, f"Missing p-1 factors for {p}")

    product = 1
    distinct_q: list[int] = []
    previous_q = 1
    for pair in factorization:
        require(
            isinstance(pair, list) and len(pair) == 2,
            f"Malformed p-1 factor entry for {p}: {pair!r}",
        )
        q, exponent = pair
        require(isinstance(q, int) and isinstance(exponent, int), f"Noninteger factor for {p}")
        require(q > previous_q, f"p-1 factors not strictly increasing for {p}")
        require(exponent >= 1, f"Invalid exponent in p-1 factorization for {p}")
        verify_prime(q, certificates, memo, active)
        product *= q**exponent
        distinct_q.append(q)
        previous_q = q

    require(product == p - 1, f"Incomplete/incorrect factorization of {p}-1")

    a = cert.get("witness")
    require(isinstance(a, int) and 1 < a < p, f"Invalid witness for {p}")
    require(pow(a, p - 1, p) == 1, f"Fermat condition failed for {p}")

    for q in distinct_q:
        value = pow(a, (p - 1) // q, p)
        require(
            math.gcd(value - 1, p) == 1,
            f"Lucas order condition failed for p={p}, q={q}",
        )

    memo.add(p)
    active.remove(p)


def factor_product(factorization: list[list[int]]) -> int:
    product = 1
    previous_p = 1
    for pair in factorization:
        require(isinstance(pair, list) and len(pair) == 2, f"Malformed factor entry: {pair!r}")
        p, exponent = pair
        require(isinstance(p, int) and isinstance(exponent, int), "Factors must be integers")
        require(p > previous_p, "Factor bases must be strictly increasing")
        require(exponent >= 1, f"Invalid exponent for factor {p}")
        product *= p**exponent
        previous_p = p
    return product


def phi_from_factorization(factorization: list[list[int]]) -> int:
    value = 1
    for p, exponent in factorization:
        value *= (p - 1) * p ** (exponent - 1)
    return value


def main() -> None:
    trajectory = load_json(TRAJECTORY_CERT)
    prime_data = load_json(PRIME_CERTS)

    require(
        trajectory.get("schema") == "erdos409-trajectory-certificate-v1",
        "Unexpected trajectory certificate schema",
    )
    require(
        prime_data.get("schema") == "lucas-pratt-prime-certificates-v1",
        "Unexpected prime-certificate schema",
    )

    claim = trajectory.get("claim")
    require(isinstance(claim, dict), "Missing claim metadata")
    require(claim.get("start") == EXPECTED_START, "Unexpected start value")
    require(claim.get("steps") == EXPECTED_STEPS, "Unexpected step count")
    require(claim.get("terminal_prime") == EXPECTED_TERMINAL, "Unexpected terminal prime")

    nodes = trajectory.get("nodes")
    require(isinstance(nodes, list), "Missing node list")
    require(len(nodes) == EXPECTED_STEPS + 1, "Trajectory must contain 69 nodes")
    require(trajectory.get("node_count") == len(nodes), "Node-count metadata mismatch")

    certificates = prime_data.get("certificates")
    require(isinstance(certificates, dict), "Missing prime-certificate map")
    memo: set[int] = set()
    active: set[int] = set()

    for index, node in enumerate(nodes):
        require(isinstance(node, dict), f"Malformed node at index {index}")
        require(node.get("index") == index, f"Index mismatch at node {index}")
        n = node.get("n")
        require(isinstance(n, int) and n >= 2, f"Invalid n at index {index}")

        factorization = node.get("factorization")
        require(isinstance(factorization, list) and factorization, f"Missing factors at index {index}")

        for p, _ in factorization:
            verify_prime(p, certificates, memo, active)

        require(
            factor_product(factorization) == n,
            f"Factorization does not multiply to n at index {index}",
        )

        if index < EXPECTED_STEPS:
            require(node.get("status") == "composite", f"Premature prime marker at index {index}")
            require(
                not (len(factorization) == 1 and factorization[0] == [n, 1]),
                f"Composite node has a prime factorization at index {index}",
            )

            phi = phi_from_factorization(factorization)
            require(node.get("phi") == phi, f"Incorrect phi at index {index}")
            expected_next = phi + 1
            require(node.get("next") == expected_next, f"Incorrect next value at index {index}")
            require(nodes[index + 1].get("n") == expected_next, f"Broken chain after index {index}")
            require(expected_next < n, f"Trajectory did not strictly decrease at index {index}")
        else:
            require(node.get("status") == "prime", "Terminal node is not marked prime")
            require(factorization == [[n, 1]], "Terminal factorization must be [p,1]")
            require(node.get("phi") is None and node.get("next") is None, "Terminal fields must be null")
            verify_prime(n, certificates, memo, active)
            require(n == EXPECTED_TERMINAL, "Wrong terminal prime")

    required_primes = prime_data.get("required_primes")
    require(isinstance(required_primes, list), "Missing required-prime list")
    actual_required = sorted(
        {p for node in nodes for p, _ in node["factorization"]}
    )
    require(required_primes == actual_required, "Required-prime inventory mismatch")

    print(
        "VERIFIED: "
        f"F({EXPECTED_START}) = {EXPECTED_STEPS}; "
        f"terminal prime = {EXPECTED_TERMINAL}; "
        f"{len(nodes)} nodes; {len(memo)} prime certificates checked."
    )


if __name__ == "__main__":
    main()
