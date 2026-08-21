import csv
import hashlib
import math
from pathlib import Path

from sympy import factorint, isprime, totient


WITNESS = 400000287233629
EXPECTED_STEPS = 104
EXPECTED_TERMINAL = 27515203921
EXPECTED_TRAJECTORY_SHA256 = "3faf8aa1b74ffa39d8e72b45b0a57ceffbc631a958f7a8bed758d3caaa745394"


def format_factorization(factors: dict[int, int]) -> str:
    return " * ".join(
        str(p) if a == 1 else f"{p}^{a}" for p, a in sorted(factors.items())
    )


def main() -> None:
    n = WITNESS
    trajectory = [n]
    computed_rows: list[dict[str, str]] = []
    while not isprime(n):
        factors = {int(p): int(a) for p, a in factorint(n).items()}
        if math.prod(p**a for p, a in factors.items()) != n:
            raise AssertionError(f"factorization does not multiply to {n}")
        phi_n = int(totient(n))
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
    print(steps, n, digest)


if __name__ == "__main__":
    main()
