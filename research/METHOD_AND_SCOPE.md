# Method, reconstruction, and scope

## Research workflow

The witness emerged from a human-directed, AI-assisted computational research process. The preserved public materials identify two broad search modes:

- forward exploration of trajectories under \(n\mapsto\varphi(n)+1\);
- inverse-totient reasoning intended to construct or extend long trajectories.

The detailed private search logs and the full original 118-entry certificate archive are not part of this repository. This publication is therefore certificate-centered: it makes the final witness directly checkable without requiring trust in the discovery process.

## Reconstruction performed for this repository

The earlier public #409 tree contained:

- a minimal SymPy verifier;
- a README describing the result;
- citation metadata;
- an MIT license;
- an AI-use disclosure.

For the correctly named repository, the mathematical packet was rebuilt from the stated start value and claim:

1. the entire orbit was recomputed;
2. every composite node was factored exactly;
3. each totient was recomputed from its factorization;
4. recursive Lucas/Pratt-style certificates were generated for every prime used;
5. a package-free certificate checker was written;
6. a second package-free implementation independently factored each node from scratch;
7. all included verification programs were executed successfully before publication.

## Why the certificate proves the exact step count

For each index \(i<68\), the certificate proves that \(n_i\) is composite and that

\[
n_{i+1}=\varphi(n_i)+1.
\]

The final node \(n_{68}=9{,}500{,}401\) has a recursively checkable primality certificate. Since none of the earlier nodes is prime and the final node is prime, the first prime is reached after exactly 68 transitions.

## Independence levels

The repository contains three checks with different trust profiles:

- `verify_certificate.py` trusts only Python integer arithmetic and the explicit certificates.
- `independent_check.py` ignores the stored factorizations and recomputes them by trial division.
- `verify.py` uses SymPy as a compact third implementation.

Agreement among these implementations is not itself a proof, but it reduces the risk of a shared coding or data-entry error. The explicit arithmetic certificate is the primary proof object.

## Scope

Finite computation can establish individual lower-bound witnesses such as this one. It cannot, by itself, resolve the open-ended asymptotic and density questions in Erdős Problem #409.
