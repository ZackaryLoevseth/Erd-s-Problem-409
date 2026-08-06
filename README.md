# An \(F=68\) witness for Erdős Problem #409

This repository contains reproducible code and exact certificates verifying

\[
\boxed{F(6{,}148{,}888{,}817)=68}
\]

for the iteration

\[
T(n)=\varphi(n)+1.
\]

Here \(F(p)=0\) when \(p\) is prime, and for composite \(n\),

\[
F(n)=1+F(T(n)).
\]

Starting from

\[
6{,}148{,}888{,}817=75{,}503\cdot81{,}439,
\]

the trajectory first reaches a prime after exactly 68 applications of \(T\). The terminal prime is

\[
9{,}500{,}401.
\]

## Verification

Three verification paths are included.

### 1. Full certificate verification — no third-party packages

```bash
python verify_certificate.py
```

This checks:

- all 69 trajectory nodes;
- the complete prime factorization of every composite node;
- every Euler-totient computation;
- every transition \(n\mapsto\varphi(n)+1\);
- the exact 68-step stopping condition;
- 213 recursive Lucas/Pratt-style primality certificates covering every prime factor and the terminal prime.

Expected output:

```text
VERIFIED: F(6148888817) = 68; terminal prime = 9500401; 69 nodes; 213 prime certificates checked.
```

### 2. Independent recomputation — no stored factors and no dependencies

```bash
python independent_check.py
```

This script factors every trajectory node from scratch by trial division and independently recomputes the complete orbit.

Expected output:

```text
68 9500401
```

### 3. Minimal SymPy check

```bash
python -m pip install -r requirements.txt
python verify.py
```

Expected output:

```text
68 9500401
```

The prime-certificate collection can also be checked separately:

```bash
python verify_pratt.py
```

## Repository contents

- [`data/certificate.json.gz`](data/certificate.json.gz) — gzip-compressed machine-readable 69-node trajectory, complete factorizations, totients, and transitions.
- [`data/prime_certificates.json.gz`](data/prime_certificates.json.gz) — gzip-compressed recursive Lucas/Pratt-style primality certificates.
- [`data/trajectory.csv`](data/trajectory.csv) — spreadsheet-friendly trajectory.
- [`data/trajectory.txt`](data/trajectory.txt) — canonical one-integer-per-line trajectory.
- [`research/TRAJECTORY_TABLE.md`](research/TRAJECTORY_TABLE.md) — complete human-readable certificate table.
- [`CLAIM_STATUS.md`](CLAIM_STATUS.md) — exact statement of what the computation proves and does not prove.
- [`research/METHOD_AND_SCOPE.md`](research/METHOD_AND_SCOPE.md) — discovery, reconstruction, verification, and scope notes.
- [`archive/ORIGINAL_PUBLICATION.md`](archive/ORIGINAL_PUBLICATION.md) — preserved text from the earlier public repository state.
- [`archive/HISTORICAL_PACKET_HASHES.md`](archive/HISTORICAL_PACKET_HASHES.md) — historical archive hashes and migration qualifications.
- [`AI_USAGE.md`](AI_USAGE.md) — authorship and AI-assistance disclosure.
- [`SHA256SUMS`](SHA256SUMS) — hashes for the reconstructed public packet.

## Mathematical significance

The certificate proves the explicit lower bound

\[
\sup_{n\ge1}F(n)\ge68.
\]

It is a computational partial result related to [Erdős Problem #409](https://www.erdosproblems.com/409) and OEIS [A039651](https://oeis.org/A039651).

The broader problem remains open. This repository does **not** provide:

- a general upper bound sharp enough to resolve the first question;
- a proof or disproof that infinitely many starting values reach a fixed prime;
- a density theorem for the basin of a fixed terminal prime;
- a proof that 68 is still the largest value known after the date of this publication.

## Provenance

The witness was publicly recorded on July 22, 2026. The earlier repository was later repurposed for Erdős Problem #64, so the #409 materials were reconstructed here under the correct repository name.

The original public tree is preserved in Git history of the renamed repository at commit

```text
905b682406251e98c9a2d1569a8a67ae82910a0e
```

This repository retains that publication’s minimal verifier and disclosure, and adds a directly inspectable certificate packet reconstructed from the stated witness.

## AI assistance and authorship

**Zackary Loevseth** directed the research target, search and verification protocol, failure correction, claim boundaries, preservation, and publication decisions.

OpenAI and Anthropic systems substantially assisted with search strategy, code generation, exact computation, independent verification, certificate construction, reproducibility checks, and technical drafting. See [`AI_USAGE.md`](AI_USAGE.md).

## Citation

```text
Zackary Loevseth, “An F = 68 witness for Erdős Problem #409,”
version 1.0.0, 2026.
https://github.com/ZackaryLoevseth/Erd-s-Problem-409
```

For the problem page:

```text
T. F. Bloom, Erdős Problem #409,
https://www.erdosproblems.com/409, accessed 2026-08-06.
```
