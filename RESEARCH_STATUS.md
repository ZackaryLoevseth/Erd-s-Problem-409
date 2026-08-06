# Research-status and claim ledger

This file separates exact results from local exhaustion statements, historical claims, and open questions.

## A. Established by the included certificates

Define $T(n)=\varphi(n)+1$, and let $F(n)$ be the first index at which the iterated trajectory reaches a prime.

The package-free certificate verifies

$$
F(6{,}668{,}696{,}999)=71
$$

with terminal prime $9{,}500{,}401$. Consequently,

$$
\sup_{n\ge1}F(n)\ge71.
$$

The same trajectory contains the nested certified records

$$
\begin{aligned}
F(6{,}148{,}888{,}817)&=68,\\
F(6{,}152{,}490{,}577)&=69,\\
F(6{,}665{,}198{,}137)&=70,\\
F(6{,}668{,}696{,}999)&=71.
\end{aligned}
$$

The proof objects include:

1. all 72 trajectory nodes;
2. complete factorization of all 71 composite nodes;
3. exact totients and transitions;
4. 222 recursive Lucas/Pratt-style prime certificates;
5. an independent factor-from-scratch implementation;
6. an independent SymPy implementation.

## B. Exact local inverse-tree result

The independent exhaustive inverse-totient verifier establishes the complete rooted tree obtained by repeatedly solving

$$
\varphi(x)=y-1
$$

starting from $y=6{,}148{,}888{,}817$. The level counts are exactly

$$
1,10,42,10,0
$$

at depths corresponding to $F=68,69,70,71,72$.

Therefore none of the ten $F=71$ values in this particular rooted tree has a direct predecessor.

## C. What the local exhaustion does not establish

The empty rooted $F=72$ level is not a global nonexistence theorem. A different $F=71$ witness, reached through another basin or discovered by forward search, may have a predecessor.

The repository does not establish:

- an upper bound sharp enough to resolve the first part of Problem #409;
- that $71$ is the global maximum of $F$;
- that no $F\ge72$ witness exists;
- that $71$ is the current world record at every later date;
- that infinitely many starting values reach any fixed prime;
- the density of any terminal-prime basin;
- a resolution of Erdős Problem #409.

## D. Historical status

The $F=68$ witness was publicly recorded on July 22, 2026. The original public repository was later renamed and repurposed for Problem #64. The historical hashes and the accessible old Git tree are preserved under [`archive/`](archive/).

The $F=69,70,71$ continuation was reconstructed and independently certified on August 5–6, 2026 from the exact inverse-totient structure above. It has not been represented here as peer-reviewed or externally human-verified.
