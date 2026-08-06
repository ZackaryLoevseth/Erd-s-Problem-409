#!/usr/bin/env python3
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESEARCH = ROOT / "research"

BASE_WITNESS = 6_148_888_817
F71_WITNESS = 6_668_696_999
EXPECTED_STEPS = 71
EXPECTED_TERMINAL = 9_500_401


def factor_list(n: int) -> list[list[int]]:
    return [[int(p), int(e)] for p, e in sorted(sp.factorint(n).items())]


def phi_from_factors(factors: list[list[int]]) -> int:
    value = 1
    for p, e in factors:
        value *= (p - 1) * p ** (e - 1)
    return value


def trajectory(start: int) -> list[dict[str, object]]:
    nodes: list[dict[str, object]] = []
    n = start
    index = 0
    while True:
        if sp.isprime(n):
            nodes.append(
                {
                    "index": index,
                    "n": n,
                    "status": "prime",
                    "factorization": [[n, 1]],
                    "phi": None,
                    "next": None,
                }
            )
            return nodes
        factors = factor_list(n)
        phi = phi_from_factors(factors)
        nxt = phi + 1
        nodes.append(
            {
                "index": index,
                "n": n,
                "status": "composite",
                "factorization": factors,
                "phi": phi,
                "next": nxt,
            }
        )
        n = nxt
        index += 1


def candidate_prime_powers(m: int) -> dict[int, list[tuple[int, int, int]]]:
    """Return p -> [(a, p**a, phi(p**a))] for every possible prime power in n with phi(n)=m."""
    options: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    for d in sp.divisors(m):
        p = int(d + 1)
        if not sp.isprime(p):
            continue
        a = 1
        power = p
        contribution = int(d)
        while m % contribution == 0:
            options[p].append((a, power, contribution))
            a += 1
            power *= p
            contribution *= p
    return dict(options)


def inverse_totients(m: int) -> list[int]:
    """Enumerate exactly all n with phi(n)=m.

    Completeness: every prime p|n satisfies p-1|m; each exponent a contributes
    phi(p**a)=p**(a-1)(p-1), and multiplicativity reduces the problem to an
    exact product selection over distinct prime powers.
    """
    options = candidate_prime_powers(m)
    primes = sorted(options, key=lambda p: min(c for _, _, c in options[p]), reverse=True)

    @lru_cache(maxsize=None)
    def search(i: int, remaining: int) -> tuple[tuple[tuple[int, int, int, int], ...], ...]:
        if i == len(primes):
            return ((),) if remaining == 1 else ()
        p = primes[i]
        out: list[tuple[tuple[int, int, int, int], ...]] = list(search(i + 1, remaining))
        for a, power, contribution in options[p]:
            if remaining % contribution:
                continue
            for tail in search(i + 1, remaining // contribution):
                out.append(((p, a, power, contribution),) + tail)
        return tuple(out)

    values: set[int] = set()
    for solution in search(0, m):
        n = math.prod(item[2] for item in solution)
        if int(sp.totient(n)) != m:
            raise AssertionError(f"internal inverse-totient error for m={m}, n={n}")
        values.add(n)
    return sorted(values)


def build_inverse_tree() -> dict[str, object]:
    levels: dict[int, list[int]] = {68: [BASE_WITNESS]}
    parent_maps: dict[int, dict[int, list[int]]] = {}
    for target_f in (69, 70, 71, 72):
        parents: dict[int, list[int]] = defaultdict(list)
        for parent in levels[target_f - 1]:
            for child in inverse_totients(parent - 1):
                parents[child].append(parent)
        parent_maps[target_f] = {k: sorted(v) for k, v in sorted(parents.items())}
        levels[target_f] = sorted(parents)

    records = []
    for f in (68, 69, 70, 71, 72):
        records.append(
            {
                "F": f,
                "count": len(levels[f]),
                "values": levels[f],
            }
        )

    edges: list[dict[str, int]] = []
    for f in (69, 70, 71, 72):
        for child, parents in parent_maps[f].items():
            for parent in parents:
                edges.append({"F": f, "child": child, "parent": parent})

    return {
        "schema": "erdos409-inverse-totient-tree-v1",
        "root": {"F": 68, "witness": BASE_WITNESS},
        "definition": "child -> parent iff phi(child)+1=parent; therefore F(child)=F(parent)+1",
        "levels": records,
        "edges": edges,
        "scope": (
            "Exact inverse-totient closure through four extension rounds rooted at the certified "
            "F=68 witness. An empty F=72 level proves only that none of the ten F=71 nodes in "
            "this rooted tree has a direct predecessor; it is not a global nonexistence result."
        ),
    }


def find_lucas_witness(p: int, factors: list[list[int]]) -> int:
    if p == 2:
        return 1
    distinct = [q for q, _ in factors]
    for a in range(2, p):
        if pow(a, p - 1, p) != 1:
            continue
        if all(math.gcd(pow(a, (p - 1) // q, p) - 1, p) == 1 for q in distinct):
            return a
    raise RuntimeError(f"no Lucas witness found for prime {p}")


def build_prime_certificates(required_primes: set[int]) -> dict[str, object]:
    certs: dict[int, dict[str, object]] = {}

    def add_prime(p: int) -> None:
        if p in certs:
            return
        if p == 2:
            certs[p] = {"p": 2, "base": True}
            return
        if not sp.isprime(p):
            raise AssertionError(f"requested non-prime certificate: {p}")
        factors = factor_list(p - 1)
        for q, _ in factors:
            add_prime(q)
        witness = find_lucas_witness(p, factors)
        certs[p] = {
            "p": p,
            "base": False,
            "p_minus_1_factorization": factors,
            "witness": witness,
        }

    for p in sorted(required_primes):
        add_prime(p)

    return {
        "schema": "lucas-pratt-prime-certificates-v2",
        "criterion": (
            "For p>2, the complete certified factorization of p-1 and a witness a satisfying "
            "a^(p-1)=1 mod p and gcd(a^((p-1)/q)-1,p)=1 for every prime q|p-1 prove p prime."
        ),
        "certificates": {str(p): certs[p] for p in sorted(certs)},
    }


def deterministic_gzip_json(path: Path, obj: object) -> None:
    raw = (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
    with path.open("wb") as out:
        with gzip.GzipFile(filename="", mode="wb", fileobj=out, mtime=0) as gz:
            gz.write(raw)


def fmt_factorization(factors: list[list[int]]) -> str:
    pieces = []
    for p, e in factors:
        pieces.append(str(p) if e == 1 else f"{p}^{e}")
    return " * ".join(pieces)


def write_trajectory_files(nodes: list[dict[str, object]]) -> None:
    with (DATA / "trajectory.txt").open("w", encoding="utf-8", newline="\n") as f:
        for node in nodes:
            f.write(f"{node['n']}\n")

    with (DATA / "trajectory.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["index", "n", "status", "factorization", "phi", "next"])
        for node in nodes:
            writer.writerow(
                [
                    node["index"],
                    node["n"],
                    node["status"],
                    fmt_factorization(node["factorization"]),
                    "" if node["phi"] is None else node["phi"],
                    "" if node["next"] is None else node["next"],
                ]
            )

    lines = [
        "# Complete certified trajectory for the F=71 witness",
        "",
        "The table records every composite factorization, exact totient, and transition.",
        "",
        "| i | n_i | status | factorization | phi(n_i) | n_{i+1} |",
        "|---:|---:|:---|:---|---:|---:|",
    ]
    for node in nodes:
        phi = "—" if node["phi"] is None else f"{node['phi']:,}"
        nxt = "—" if node["next"] is None else f"{node['next']:,}"
        lines.append(
            f"| {node['index']} | {node['n']:,} | {node['status']} | "
            f"`{fmt_factorization(node['factorization'])}` | {phi} | {nxt} |"
        )
    (RESEARCH / "TRAJECTORY_TABLE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_inverse_tree_csv(tree: dict[str, object]) -> None:
    with (DATA / "inverse_tree_edges.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["F_child", "child", "parent", "phi_child"])
        for edge in tree["edges"]:
            writer.writerow([edge["F"], edge["child"], edge["parent"], edge["parent"] - 1])



def write_inverse_tree_nodes_csv(tree: dict[str, object]) -> None:
    parent_counts: dict[tuple[int, int], int] = defaultdict(int)
    for edge in tree["edges"]:
        parent_counts[(int(edge["F"]), int(edge["child"]))] += 1
    with (DATA / "inverse_tree_nodes.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["F", "value", "factorization", "parent_count"])
        for level in tree["levels"]:
            f_value = int(level["F"])
            for value in level["values"]:
                factors = factor_list(int(value))
                writer.writerow([
                    f_value,
                    value,
                    fmt_factorization(factors),
                    parent_counts.get((f_value, int(value)), 0),
                ])


def write_record_chain_csv(record_chain: list[dict[str, int]], nodes: list[dict[str, object]]) -> None:
    by_n = {int(node["n"]): node for node in nodes}
    with (DATA / "record_chain.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["F", "witness", "factorization", "phi", "next"])
        for item in sorted(record_chain, key=lambda x: int(x["F"]), reverse=True):
            node = by_n[int(item["witness"])]
            writer.writerow([
                item["F"],
                item["witness"],
                fmt_factorization(node["factorization"]),
                node["phi"],
                node["next"],
            ])

def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    RESEARCH.mkdir(parents=True, exist_ok=True)

    nodes = trajectory(F71_WITNESS)
    if len(nodes) - 1 != EXPECTED_STEPS or nodes[-1]["n"] != EXPECTED_TERMINAL:
        raise AssertionError((len(nodes) - 1, nodes[-1]["n"]))
    if nodes[3]["n"] != BASE_WITNESS:
        raise AssertionError("F=71 chain does not enter the certified F=68 witness at step 3")

    record_chain = [
        {"F": 68, "witness": nodes[3]["n"]},
        {"F": 69, "witness": nodes[2]["n"]},
        {"F": 70, "witness": nodes[1]["n"]},
        {"F": 71, "witness": nodes[0]["n"]},
    ]
    certificate = {
        "schema": "erdos409-trajectory-certificate-v2",
        "claim": {
            "start": F71_WITNESS,
            "steps": EXPECTED_STEPS,
            "terminal_prime": EXPECTED_TERMINAL,
        },
        "record_chain": record_chain,
        "nodes": nodes,
    }

    required_primes: set[int] = set()
    for node in nodes:
        for p, _ in node["factorization"]:
            required_primes.add(p)
    prime_certs = build_prime_certificates(required_primes)
    tree = build_inverse_tree()

    if len(tree["levels"][1]["values"]) != 10:
        raise AssertionError("unexpected F=69 inverse-tree count")
    if len(tree["levels"][2]["values"]) != 42:
        raise AssertionError("unexpected F=70 inverse-tree count")
    if len(tree["levels"][3]["values"]) != 10:
        raise AssertionError("unexpected F=71 inverse-tree count")
    if len(tree["levels"][4]["values"]) != 0:
        raise AssertionError("unexpected F=72 inverse-tree count")
    if F71_WITNESS not in tree["levels"][3]["values"]:
        raise AssertionError("chosen F=71 witness missing from exact inverse tree")

    deterministic_gzip_json(DATA / "trajectory_certificate.json.gz", certificate)
    deterministic_gzip_json(DATA / "prime_certificates.json.gz", prime_certs)
    deterministic_gzip_json(DATA / "inverse_totient_tree.json.gz", tree)
    write_trajectory_files(nodes)
    write_inverse_tree_csv(tree)
    write_inverse_tree_nodes_csv(tree)
    write_record_chain_csv(record_chain, nodes)

    summary = {
        "claim": certificate["claim"],
        "record_chain": record_chain,
        "trajectory_nodes": len(nodes),
        "prime_certificates": len(prime_certs["certificates"]),
        "inverse_tree_level_counts": {
            str(level["F"]): level["count"] for level in tree["levels"]
        },
    }
    (DATA / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
