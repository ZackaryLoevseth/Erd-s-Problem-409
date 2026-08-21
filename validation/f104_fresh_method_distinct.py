#!/usr/bin/env python3
"""Fresh standard-library audit for the Erdős #409 F=104 packet.

This implementation intentionally shares no evaluator code with the packet.
It factors every composite trajectory node with deterministic Pollard--Rho,
uses deterministic Miller--Rabin for all 64-bit primality decisions, parses
and checks every exported factorization, recomputes every Euler totient and
transition, and checks packet metadata.  It also runs six semantic mutations.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any


EXPECTED_WITNESS = 400_000_287_233_629
EXPECTED_STEPS = 104
EXPECTED_TERMINAL = 27_515_203_921
EXPECTED_NODES = 105
EXPECTED_TRAJECTORY_SHA256 = (
    "3faf8aa1b74ffa39d8e72b45b0a57ceffbc631a958f7a8bed758d3caaa745394"
)

# This base set is deterministic for every unsigned 64-bit integer.
MR_BASES = (2, 325, 9_375, 28_178, 450_775, 9_780_504, 1_795_265_022)
SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


class AuditFailure(AssertionError):
    """A packet or mutation failed a semantic validation gate."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def is_prime_64(n: int) -> bool:
    if n < 2:
        return False
    for prime in SMALL_PRIMES:
        if n % prime == 0:
            return n == prime
    d = n - 1
    power = 0
    while d % 2 == 0:
        d //= 2
        power += 1
    for raw_base in MR_BASES:
        base = raw_base % n
        if base == 0:
            continue
        value = pow(base, d, n)
        if value in (1, n - 1):
            continue
        for _ in range(power - 1):
            value = value * value % n
            if value == n - 1:
                break
        else:
            return False
    return True


def primes_through(limit: int) -> list[int]:
    """Return all primes through ``limit`` with an Eratosthenes sieve."""
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if not sieve[prime]:
            continue
        first = prime * prime
        sieve[first : limit + 1 : prime] = b"\x00" * (((limit - first) // prime) + 1)
    return [value for value, flag in enumerate(sieve) if flag]


def pollard_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    # Fixed parameters keep the audit deterministic and replayable.
    for c in range(1, 128):
        x = 2 + c
        y = x
        divisor = 1
        for _ in range(1_000_000):
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            divisor = math.gcd(abs(x - y), n)
            if divisor != 1:
                break
        if 1 < divisor < n:
            return divisor
    raise AuditFailure(f"deterministic Pollard--Rho failed to split {n}")


def factor_from_scratch(n: int) -> Counter[int]:
    output: Counter[int] = Counter()
    stack = [n]
    while stack:
        value = stack.pop()
        if value == 1:
            continue
        if is_prime_64(value):
            output[value] += 1
            continue
        divisor = pollard_rho(value)
        stack.extend((divisor, value // divisor))
    return Counter(dict(sorted(output.items())))


def parse_factorization(text: str) -> Counter[int]:
    factors: Counter[int] = Counter()
    for raw_term in text.split(" * "):
        term = raw_term.strip()
        require(bool(term), "empty factorization term")
        if "^" in term:
            raw_prime, raw_exponent = term.split("^", 1)
            prime = int(raw_prime)
            exponent = int(raw_exponent)
        else:
            prime = int(term)
            exponent = 1
        require(exponent >= 1, f"invalid exponent in {text!r}")
        require(is_prime_64(prime), f"listed factor is not prime: {prime}")
        factors[prime] += exponent
    return Counter(dict(sorted(factors.items())))


def phi_from_factors(n: int, factors: Counter[int]) -> int:
    product = math.prod(prime**exponent for prime, exponent in factors.items())
    require(product == n, f"factors multiply to {product}, not {n}")
    result = n
    for prime in factors:
        result = result // prime * (prime - 1)
    return result


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    require(
        set(rows[0]) == {"index", "n", "is_prime", "factorization", "phi_n", "next_n"},
        "trajectory schema mismatch",
    )
    return rows


def validate_semantics(
    rows: list[dict[str, str]],
    report: dict[str, Any],
    terminal_evidence: dict[str, Any],
) -> dict[str, Any]:
    require(len(rows) == int(report["trajectory_nodes"]), "report node count mismatch")
    require(len(rows) == EXPECTED_NODES, "trajectory must contain 105 nodes")
    require(int(report["F"]) == EXPECTED_STEPS, "claimed stopping time is not 104")
    require(int(report["witness"]) == EXPECTED_WITNESS, "report witness mismatch")
    require(int(report["terminal_prime"]) == EXPECTED_TERMINAL, "report terminal mismatch")

    values: list[int] = []
    composite_count = 0
    factor_count = 0
    for position, row in enumerate(rows):
        require(int(row["index"]) == position, f"bad index at row {position}")
        n = int(row["n"])
        values.append(n)
        primality = is_prime_64(n)
        require(row["is_prime"] == str(primality), f"primality flag mismatch at {position}")

        exported_factors = parse_factorization(row["factorization"])
        fresh_factors = factor_from_scratch(n)
        require(exported_factors == fresh_factors, f"factorization mismatch at {position}")
        factor_count += sum(exported_factors.values())

        if primality:
            require(position == len(rows) - 1, f"prime occurs before terminal row {position}")
            require(row["phi_n"] == "" and row["next_n"] == "", "terminal fields not empty")
            continue

        composite_count += 1
        require(position + 1 < len(rows), "composite final row")
        phi_n = phi_from_factors(n, exported_factors)
        require(int(row["phi_n"]) == phi_n, f"totient mismatch at {position}")
        require(int(row["next_n"]) == phi_n + 1, f"transition field mismatch at {position}")
        require(int(rows[position + 1]["n"]) == phi_n + 1, f"next row mismatch at {position}")

    steps = len(values) - 1
    digest = hashlib.sha256(",".join(map(str, values)).encode("ascii")).hexdigest()
    require(values[0] == EXPECTED_WITNESS, "trajectory witness mismatch")
    require(steps == EXPECTED_STEPS, "computed stopping time mismatch")
    require(values[-1] == EXPECTED_TERMINAL, "computed terminal mismatch")
    require(digest == EXPECTED_TRAJECTORY_SHA256, "trajectory digest mismatch")
    require(report["trajectory_sha256"] == digest, "report trajectory digest mismatch")

    require(int(terminal_evidence["n"]) == values[-1], "terminal evidence n mismatch")
    require(terminal_evidence["result"] == "prime", "terminal evidence result mismatch")
    require(
        terminal_evidence["method"]
        == "deterministic trial division by every prime p <= floor(sqrt(n))",
        "terminal evidence method mismatch",
    )
    require(
        int(terminal_evidence["floor_sqrt_n"]) == math.isqrt(values[-1]),
        "terminal evidence square-root bound mismatch",
    )
    terminal_trial_primes = primes_through(math.isqrt(values[-1]))
    require(
        len(terminal_trial_primes) == int(terminal_evidence["number_of_primes_tested"]),
        "terminal evidence prime-test count mismatch",
    )
    require(
        terminal_trial_primes[-1] == int(terminal_evidence["largest_prime_tested"]),
        "terminal evidence largest tested prime mismatch",
    )
    require(
        all(values[-1] % prime for prime in terminal_trial_primes),
        "terminal has a divisor at or below its square root",
    )
    require(is_prime_64(values[-1]), "terminal failed deterministic 64-bit primality test")

    return {
        "F": steps,
        "composite_nodes_checked": composite_count,
        "factor_occurrences_checked": factor_count,
        "status": "PASS_FRESH_METHOD_DISTINCT_REPLAY",
        "terminal_prime": values[-1],
        "terminal_trial_division_primes_checked": len(terminal_trial_primes),
        "trajectory_nodes": len(values),
        "trajectory_sha256": digest,
        "witness": values[0],
    }


def run_mutations(
    original_rows: list[dict[str, str]],
    original_report: dict[str, Any],
    original_terminal: dict[str, Any],
) -> dict[str, str]:
    cases: dict[str, tuple[list[dict[str, str]], dict[str, Any], dict[str, Any]]] = {}

    rows = deepcopy(original_rows)
    rows[50]["n"] = str(int(rows[50]["n"]) + 2)
    cases["alter_trajectory_value"] = (rows, deepcopy(original_report), deepcopy(original_terminal))

    rows = deepcopy(original_rows)
    rows[0]["factorization"] = "1399663 * 285783281"
    cases["alter_factor"] = (rows, deepcopy(original_report), deepcopy(original_terminal))

    rows = deepcopy(original_rows)
    rows[104]["factorization"] = "27515203919"
    cases["alter_prime"] = (rows, deepcopy(original_report), deepcopy(original_terminal))

    rows = deepcopy(original_rows)
    del rows[50]
    for index, row in enumerate(rows):
        row["index"] = str(index)
    report = deepcopy(original_report)
    report["trajectory_nodes"] = len(rows)
    cases["remove_node"] = (rows, report, deepcopy(original_terminal))

    rows = deepcopy(original_rows)
    rows[-1]["n"] = "27515203923"
    rows[-1]["factorization"] = "27515203923"
    cases["change_terminal_value"] = (rows, deepcopy(original_report), deepcopy(original_terminal))

    report = deepcopy(original_report)
    report["F"] = 103
    cases["change_claimed_stopping_time"] = (
        deepcopy(original_rows), report, deepcopy(original_terminal)
    )

    result: dict[str, str] = {}
    for name, (rows, report, terminal) in cases.items():
        try:
            validate_semantics(rows, report, terminal)
        except (AuditFailure, KeyError, ValueError, TypeError) as exc:
            result[name] = f"REJECTED: {type(exc).__name__}: {exc}"
        else:
            raise AuditFailure(f"mutation was incorrectly accepted: {name}")
    require(len(result) == 6, "not all mutation categories ran")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    packet = args.packet.resolve()
    rows = load_rows(packet / "trajectory.csv")
    report = json.loads((packet / "final_validation_report.json").read_text(encoding="utf-8"))
    terminal = json.loads((packet / "terminal_primality.json").read_text(encoding="utf-8"))
    replay = validate_semantics(rows, report, terminal)
    mutations = run_mutations(rows, report, terminal)
    output = {
        "implementation": (
            "fresh standard-library deterministic Pollard--Rho factorization plus "
            "deterministic 64-bit Miller--Rabin"
        ),
        "mutations": mutations,
        "replay": replay,
        "status": "PASS_F104_FRESH_REPLAY_AND_6_OF_6_MUTATIONS_REJECTED",
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
