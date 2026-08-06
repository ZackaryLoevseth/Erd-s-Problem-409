# Archived original publication text

**Source:** Git commit `905b682406251e98c9a2d1569a8a67ae82910a0e` in the repository later renamed `Erd-s-Problem-64`.

The text below is preserved for provenance. Links and availability claims reflect the earlier repository state and may no longer be current.

---

# An F = 68 witness for Erdős Problem #409

Certificates and code verifying

$$
F(6{,}148{,}888{,}817)=68
$$

for the iteration

$$
T(n)=\varphi(n)+1.
$$

Here $F(p)=0$ when $p$ is prime, and for composite $n$,

$$
F(n)=1+F(T(n)).
$$

Starting from

$$
6{,}148{,}888{,}817
=
75{,}503 \times 81{,}439,
$$

the trajectory first reaches a prime after exactly 68 applications of $T$.

The terminal prime is

$$
9{,}500{,}401.
$$

## Minimal verification

The verification program is contained in [`verify.py`](verify.py).

From a terminal opened in this repository, run:

```bash
python -m pip install -r requirements.txt
python verify.py
```

Expected output:

```text
68 9500401
```

The complete verification code is:

```python
from sympy import isprime, totient


def main() -> None:
    n = 6_148_888_817
    steps = 0

    while not isprime(n):
        n = int(totient(n)) + 1
        steps += 1

    print(steps, n)

    if (steps, n) != (68, 9_500_401):
        raise RuntimeError(
            f"Unexpected result: expected (68, 9500401), got ({steps}, {n})"
        )


if __name__ == "__main__":
    main()
```

## Scope of the result

This establishes the explicit computational lower bound

$$
\sup_{n\ge1}F(n)\ge68.
$$

It is a computational partial result related to [Erdős Problem #409](https://www.erdosproblems.com/409).

It does **not** resolve the broader questions concerning:

- upper bounds for $F(n)$;
- whether infinitely many integers reach the same terminal prime;
- the density of integers reaching a fixed prime.

I am not currently aware of a previously published example with $F\ge68$. 

## Verification packet

The complete certificate packet contains:

- the full 69-node trajectory;
- exact factorizations of every composite trajectory node;
- exact recomputation of every totient;
- verification of every transition;
- independent implementations;
- a standalone certificate checker;
- a terminal-primality certificate;
- a 118-entry SHA-256 manifest.

Archive SHA-256:

```text
ca5b9a9e69f9a91e3de2642452259c307a416f659349c5067cb20c692f42d026
```

Canonical trajectory SHA-256:

```text
6a6758b8bb6e2d2cd812301b04eabc9d14699d18908a1cdf7066454934802ad7
```

The complete certificate archive is provided through this repository’s GitHub Releases section.

## AI assistance and authorship

This result was produced through a substantially AI-assisted research workflow using OpenAI and Anthropic systems.

The research target, governing protocol, iterative prompt design, verification requirements, cross-model review, and final publication decisions were directed by **Zackary Loevseth**.

## Public record

This witness was posted on the discussion page for
[Erdős Problem #409](https://www.erdosproblems.com/409) on July 22, 2026.

It is as an example giving the largest known value
of \(F(n)\).

## Citation

T. F. Bloom, “Erdős Problem #409,”  
https://www.erdosproblems.com/409, accessed July 22, 2026.
