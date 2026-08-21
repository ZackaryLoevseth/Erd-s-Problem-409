import csv
import hashlib
import json
import math
from pathlib import Path


WITNESS = 400000287233629
EXPECTED_STEPS = 104
EXPECTED_TERMINAL = 27515203921
EXPECTED_TRAJECTORY_SHA256 = "3faf8aa1b74ffa39d8e72b45b0a57ceffbc631a958f7a8bed758d3caaa745394"


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (
                ((limit - start) // p) + 1
            )
    return [i for i, flag in enumerate(sieve) if flag]


PRIMES = primes_up_to(math.isqrt(WITNESS) + 1)


def factorint_trial(n: int) -> dict[int, int]:
    remaining = n
    factors: dict[int, int] = {}
    for p in PRIMES:
        if p * p > remaining:
            break
        if remaining % p == 0:
            exponent = 0
            while remaining % p == 0:
                remaining //= p
                exponent += 1
            factors[p] = exponent
        if remaining == 1:
            break
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    for p in PRIMES:
        if p * p > n:
            break
        if n % p == 0:
            return n == p
    return True


def phi_from_factorization(n: int, factors: dict[int, int]) -> int:
    if math.prod(p**a for p, a in factors.items()) != n:
        raise AssertionError(f"factorization does not multiply to {n}")
    result = n
    for p in factors:
        result = (result // p) * (p - 1)
    return result


def format_factorization(factors: dict[int, int]) -> str:
    return " * ".join(
        str(p) if a == 1 else f"{p}^{a}" for p, a in sorted(factors.items())
    )


def main() -> None:
    n = WITNESS
    trajectory = [n]
    computed_rows: list[dict[str, str]] = []
    while not is_prime_trial(n):
        factors = factorint_trial(n)
        phi_n = phi_from_factorization(n, factors)
        next_n = phi_n + 1
        computed_rows.append(
            {
                "n": str(n),
                "is_prime": "False",
                "factorization": format_factorization(factors),
                "phi_n": str(phi_n),
                "next_n": str(next_n),
            }
        )
        n = next_n
        trajectory.append(n)
    computed_rows.append(
        {
            "n": str(n),
            "is_prime": "True",
            "factorization": str(n),
            "phi_n": "",
            "next_n": "",
        }
    )

    steps = len(trajectory) - 1
    digest = hashlib.sha256(
        ",".join(str(x) for x in trajectory).encode("ascii")
    ).hexdigest()
    if (steps, n, digest) != (
        EXPECTED_STEPS,
        EXPECTED_TERMINAL,
        EXPECTED_TRAJECTORY_SHA256,
    ):
        raise AssertionError(
            f"expected {(EXPECTED_STEPS, EXPECTED_TERMINAL, EXPECTED_TRAJECTORY_SHA256)}, "
            f"got {(steps, n, digest)}"
        )

    with Path(__file__).with_name("trajectory.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        exported = list(csv.DictReader(handle))
    if len(exported) != len(computed_rows):
        raise AssertionError("trajectory.csv row count mismatch")
    for index, (row, computed) in enumerate(zip(exported, computed_rows)):
        if row["index"] != str(index):
            raise AssertionError(f"bad index in trajectory.csv row {index}")
        for key, expected in computed.items():
            if row[key] != expected:
                raise AssertionError(
                    f"trajectory.csv row {index} field {key}: "
                    f"expected {expected!r}, got {row[key]!r}"
                )

    print(
        json.dumps(
            {
                "F": steps,
                "status": "PASS",
                "terminal_prime": n,
                "trajectory_nodes": len(trajectory),
                "trajectory_sha256": digest,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
