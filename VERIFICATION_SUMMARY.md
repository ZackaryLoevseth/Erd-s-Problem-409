# Verification summary

The F=104 public-release candidate passed:

- exact validation of all nine files in the canonical private packet manifest;
- the original SymPy evaluator;
- the original dependency-free trial-division evaluator;
- a fresh method-distinct standard-library implementation using deterministic
  Pollard–Rho factorization and deterministic 64-bit Miller–Rabin;
- recomputation of all 104 composite-node factorizations, totients, and
  transitions;
- independent checking of 310 prime-factor occurrences;
- independent terminal-prime trial division by all 15,165 primes through
  `floor(sqrt(27515203921))=165877`;
- all 105 nodes, first-prime location, terminal value, stopping time, and
  trajectory digest;
- rejection of all six required mutations: one trajectory value, one factor,
  one prime, one removed node, terminal value, and claimed stopping time;
- canonical and fresh replay after clean extraction;
- no absolute-path dependency and identical pre/post extracted-tree digest.

Canonical packet tree SHA-256: 
`5e42d868475f58b9df0bf1d78e4481b479040854600d852e13eebebc8fb6c9cd`.

Clean-extraction source-tree SHA-256 before and after replay:
`5e42d868475f58b9df0bf1d78e4481b479040854600d852e13eebebc8fb6c9cd`.

The public packet intentionally excludes the private search-scope note because
its inverse-enumeration claims were not needed for, and were not promoted with,
the freshly validated pointwise F=104 result.
