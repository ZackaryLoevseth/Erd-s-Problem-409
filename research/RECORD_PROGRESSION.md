# Certified record progression from F=68 through F=71

## The four witnesses

| F-value | Witness $n$ | Exact factorization | $\varphi(n)$ | $T(n)$ |
|---:|---:|:---|---:|---:|
| 71 | 6,668,696,999 | $1907\cdot3{,}496{,}957$ | 6,665,198,136 | 6,665,198,137 |
| 70 | 6,665,198,137 | $13\cdot512{,}707{,}549$ | 6,152,490,576 | 6,152,490,577 |
| 69 | 6,152,490,577 | $1709\cdot3{,}600{,}053$ | 6,148,888,816 | 6,148,888,817 |
| 68 | 6,148,888,817 | $75{,}503\cdot81{,}439$ | 6,148,731,876 | 6,148,731,877 |

The final row then follows the previously certified 68-step trajectory to the prime $9{,}500{,}401$.

## Why each extension raises F by exactly one

If $T(x)=y$ and $y$ first reaches a prime after exactly $r$ further iterations, then $x$ first reaches a prime after exactly $r+1$ iterations, provided $x$ is composite. Every displayed witness has a complete composite factorization, and every arrow is checked exactly.

Thus

$$
F(6{,}668{,}696{,}999)
=1+F(6{,}665{,}198{,}137)
=2+F(6{,}152{,}490{,}577)
=3+F(6{,}148{,}888{,}817)
=71.
$$

## Certification layers

The result is not inferred from decimal output alone. The repository checks:

- exact products for every factorization;
- recursive primality certificates for every stated prime factor;
- the Euler-product formula for every totient;
- the complete ordered trajectory;
- the first-prime stopping condition;
- independent recomputation without stored factors.

The full 72-node table is in [`TRAJECTORY_TABLE.md`](TRAJECTORY_TABLE.md).
