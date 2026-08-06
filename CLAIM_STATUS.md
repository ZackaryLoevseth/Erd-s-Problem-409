# Claim-status ledger

## Established by the included certificate

Let

\[
T(n)=\varphi(n)+1,
\]

and define \(F(p)=0\) for prime \(p\), while

\[
F(n)=1+F(T(n))
\]

for composite \(n\).

The files in this repository certify

\[
F(6{,}148{,}888{,}817)=68
\]

with terminal prime \(9{,}500{,}401\).

This is established by:

1. a 69-node exact trajectory;
2. complete prime factorizations for all 68 composite nodes;
3. direct recomputation of every Euler totient;
4. exact validation of all 68 transitions;
5. recursive Lucas/Pratt-style primality certificates for every factor and the terminal prime;
6. an independent factor-from-scratch recomputation.

Therefore the explicit lower bound

\[
\sup_{n\ge1}F(n)\ge68
\]

is also established.

## Not established

This repository does not establish:

- any optimal general upper bound for \(F(n)\);
- that 68 is the global maximum of \(F\);
- that 68 remains the largest published computational value at all later dates;
- whether infinitely many \(n\) reach the same terminal prime;
- the density of the set of \(n\) reaching any fixed prime;
- a resolution of Erdős Problem #409.

## Historical-record qualification

The July 2026 publication described the witness as giving the largest known value at that time. The present repository preserves that statement as provenance, not as an indefinitely current literature claim.
