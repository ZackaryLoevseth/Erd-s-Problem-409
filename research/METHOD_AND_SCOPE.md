# Method, verification architecture, and scope

## Research workflow

The project uses two complementary search directions.

### Forward iteration

For a chosen start $n$, repeatedly compute $\varphi(n)+1$, memoize previously resolved tails, and record stopping times and terminal primes. Forward search is broad but can spend substantial work rediscovering short or already known basins.

### Inverse-totient extension

For a node $y$ on a long certified path, solve $\varphi(x)=y-1$. Every composite solution prepends one exact step. This can extend records efficiently, but a single inverse tree may terminate even when other basins continue.

The current $F=69,70,71$ progression was obtained by exact inverse extension of the earlier $F=68$ witness.

## Verification architecture

### Primary arithmetic certificate

`data/trajectory_certificate.json.gz` records the ordered trajectory, complete prime factorizations, exact totients, and transitions.

### Recursive primality certificates

`data/prime_certificates.json.gz` contains complete factorizations of $p-1$ and Lucas witnesses. The package-free verifier recursively proves every prime used in the trajectory certificate.

### Independent trajectory recomputation

`independent_check.py` ignores the stored factors, factors every node from scratch by trial division, and independently reconstructs the full trajectory.

### Independent inverse-tree recomputation

The generator uses a recursive exact-product enumeration. `verify_inverse_tree.py` uses a separate dynamic-programming algorithm and package-free 64-bit primality testing to regenerate all rooted inverse levels and edges.

### Compact third implementation

`verify.py` performs the full iteration with SymPy.

### Integrity

`SHA256SUMS` binds the public files, and GitHub Actions runs every verifier on pushes to `main` and on pull requests.

## Scope discipline

The following distinctions are essential:

- A **trajectory certificate** proves the stopping time of one starting value.
- An **inverse-tree enumeration** proves completeness only within its declared rooted construction.
- A **record lower bound** does not prove a global maximum.
- Multiple starts reaching one prime do not prove an infinite basin.
- Finite frequency data does not prove an asymptotic density.
- Passing CI verifies the published code and data; it is not a substitute for external mathematical review of the completeness argument.

## Recovery and reconstruction

The original July 2026 public tree preserved only a minimal $F=68$ verifier and publication metadata. The larger historical archive named in that README was not present in the accessible GitHub release state during migration. The current packet therefore rebuilds the arithmetic directly and records its own hashes rather than claiming byte identity with the missing historical archive.
