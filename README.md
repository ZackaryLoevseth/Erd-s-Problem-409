# Erdős Problem #409 — research archive and certified record computations

[![Verify research packet](https://github.com/ZackaryLoevseth/Erd-s-Problem-409/actions/workflows/verify.yml/badge.svg)](https://github.com/ZackaryLoevseth/Erd-s-Problem-409/actions/workflows/verify.yml)

> **Status:** Erdős Problem #409 remains open. This repository contains a reproducible computational research record, including certified stopping-time witnesses through $F=71$, an exact rooted inverse-totient tree, search protocols, and claim boundaries. It does **not** claim to solve the full problem.

## The problem

For

$$
T(n)=\varphi(n)+1,
$$

let $F(n)$ be the number of iterations required to reach a prime. Erdős Problem #409 asks three related questions:

1. **Stopping time:** how large can $F(n)$ be, and what useful upper bounds hold?
2. **Common terminal primes:** can infinitely many starting values reach the same prime?
3. **Density:** what is the density of the starting values that reach a fixed prime?

This repository is organized around the complete problem, not around a single witness.

## Current certified research state

The strongest trajectory certificate presently included is

$$
\boxed{F(6{,}668{,}696{,}999)=71}.
$$

It extends the earlier $F=68$ witness by three exact inverse-totient steps:

$$
\begin{aligned}
6{,}668{,}696{,}999
&\longmapsto 6{,}665{,}198{,}137\\
&\longmapsto 6{,}152{,}490{,}577\\
&\longmapsto 6{,}148{,}888{,}817,
\end{aligned}
$$

where each arrow is $n\mapsto\varphi(n)+1$. The last value is the previously certified $F=68$ witness, so the four nested records are:

| Certified value | Witness |
|---:|---:|
| $F=68$ | $6{,}148{,}888{,}817$ |
| $F=69$ | $6{,}152{,}490{,}577$ |
| $F=70$ | $6{,}665{,}198{,}137$ |
| $F=71$ | $6{,}668{,}696{,}999$ |

All four trajectories terminate at the prime

$$
9{,}500{,}401.
$$

### Exact rooted inverse-totient continuation

Starting from the certified $F=68$ witness, the included exhaustive inverse-totient computation gives:

| Level | Exact number of values in this rooted tree |
|---:|---:|
| $F=68$ | 1 |
| $F=69$ | 10 |
| $F=70$ | 42 |
| $F=71$ | 10 |
| direct $F=72$ extensions | 0 |

The empty final level means only that none of these ten rooted $F=71$ values has a direct inverse-totient predecessor. It does **not** prove that no $F=72$ witness exists elsewhere.

See [`research/RECORD_PROGRESSION.md`](research/RECORD_PROGRESSION.md) and [`research/INVERSE_TOTIENT_TREE.md`](research/INVERSE_TOTIENT_TREE.md).

## Verification

The primary verification paths require only Python's standard library.

```bash
python verify_manifest.py
python verify_certificate.py
python verify_pratt.py
python verify_inverse_tree.py
python independent_check.py
```

Expected core outputs include:

```text
VERIFIED: F(6668696999)=71; terminal prime=9500401; 72 nodes; 222 prime certificates used.
VERIFIED inverse tree: F68=1, F69=10, F70=42, F71=10, F72=0; 62 exact parent-child edges.
71 9500401
```

A compact independent SymPy check is also included:

```bash
python -m pip install -r requirements.txt
python verify.py
```

Every push and pull request runs all checks in GitHub Actions.

## Repository map

### Research record

- [`RESEARCH_STATUS.md`](RESEARCH_STATUS.md) — exactly what is established, locally exhausted, historical, or still open.
- [`research/PROBLEM_MAP.md`](research/PROBLEM_MAP.md) — the three subproblems and how the current work bears on each.
- [`research/RECORD_PROGRESSION.md`](research/RECORD_PROGRESSION.md) — the certified $F=68,69,70,71$ chain.
- [`research/INVERSE_TOTIENT_TREE.md`](research/INVERSE_TOTIENT_TREE.md) — exact enumeration theorem, counts, scope, and limitations.
- [`research/CONTINUATION_PROTOCOL.md`](research/CONTINUATION_PROTOCOL.md) — the autonomous search and certification protocol for $F\ge72$.
- [`research/METHOD_AND_SCOPE.md`](research/METHOD_AND_SCOPE.md) — discovery, inverse search, verification, and epistemic boundaries.
- [`research/TRAJECTORY_TABLE.md`](research/TRAJECTORY_TABLE.md) — all 72 trajectory nodes with exact arithmetic.

### Data

- [`data/trajectory_certificate.json.gz`](data/trajectory_certificate.json.gz) — complete 72-node certificate.
- [`data/prime_certificates.json.gz`](data/prime_certificates.json.gz) — 222 recursive Lucas/Pratt-style primality certificates.
- [`data/inverse_totient_tree.json.gz`](data/inverse_totient_tree.json.gz) — exact rooted levels and 62 parent-child edges.
- [`data/trajectory.csv`](data/trajectory.csv) and [`data/trajectory.txt`](data/trajectory.txt) — human- and machine-readable orbit data.
- [`data/inverse_tree_nodes.csv`](data/inverse_tree_nodes.csv) and [`data/inverse_tree_edges.csv`](data/inverse_tree_edges.csv) — flat rooted-tree tables.
- [`data/record_chain.csv`](data/record_chain.csv) — the certified F=68 through F=71 progression.
- [`data/summary.json`](data/summary.json) — concise packet summary.

### Verification and reproduction

- [`verify_certificate.py`](verify_certificate.py) — package-free trajectory and prime-certificate verification.
- [`verify_inverse_tree.py`](verify_inverse_tree.py) — independent package-free exhaustive inverse-totient recomputation.
- [`independent_check.py`](independent_check.py) — factor-from-scratch trajectory recomputation.
- [`verify.py`](verify.py) — minimal SymPy implementation.
- [`tools/generate_packet.py`](tools/generate_packet.py) — deterministic data and certificate generator.
- [`SHA256SUMS`](SHA256SUMS) — integrity manifest.

### Historical record

- [`archive/F68_PUBLICATION_HISTORY.md`](archive/F68_PUBLICATION_HISTORY.md) — the July 2026 $F=68$ publication and its later migration.
- [`archive/HISTORICAL_PACKET_HASHES.md`](archive/HISTORICAL_PACKET_HASHES.md) — preserved hashes and precise availability qualifications.

## Mathematical significance and limits

The certificate establishes the explicit lower bound

$$
\sup_{n\ge1}F(n)\ge71.
$$

It also provides an exactly enumerated local inverse tree rooted at one previously certified witness. These are finite computational results relevant to the stopping-time part of Problem #409.

They do not establish a general upper bound, a global maximum, the nonexistence of $F\ge72$, infinitude of any terminal-prime basin, or a density theorem. The public packet also makes no claim that $71$ is the current world record without a separate, current literature comparison.

## Authorship and AI assistance

**Zackary Loevseth** directed the research target, execution protocol, failure correction, verification requirements, preservation, claim boundaries, and publication decisions. OpenAI and Anthropic systems substantially assisted with search, code, exact computation, independent checking, certificate construction, recovery, and drafting. See [`AI_USAGE.md`](AI_USAGE.md).

## References

- T. F. Bloom, [Erdős Problem #409](https://www.erdosproblems.com/409), accessed 2026-08-06.
- OEIS [A039651](https://oeis.org/A039651), number of iterations of $n\mapsto\varphi(n)+1$ required to reach a prime.
- OEIS [A039650](https://oeis.org/A039650), terminal prime reached by the iteration.

## Suggested citation

```text
Zackary Loevseth, “Erdős Problem #409 — research archive and
certified record computations through F=71,” version 2.0.0, 2026.
https://github.com/ZackaryLoevseth/Erd-s-Problem-409
```
