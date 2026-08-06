# Autonomous continuation protocol for F >= 72

## Mission

Starting from the certified result

$$
F(6{,}668{,}696{,}999)=71,
$$

search for and exactly certify witnesses attaining $F=72$, then $73$, then $74$, continuing automatically while the available environment can make certified progress.

## Non-termination rules

The search must not stop merely because:

- one record witness has no inverse-totient predecessor;
- the rooted inverse tree published here is exhausted;
- one algorithm, congruence class, size range, or basin fails;
- a candidate cannot be certified;
- a heuristic ceases to improve.

Failure of a branch is evidence about that branch, not evidence that the target value is impossible.

## Search lanes

1. **Complete inverse extension of every available record witness.** Enumerate all inverse totients of $y-1$, not only the smallest or first solution.
2. **Alternative depth-71 basins.** Search for other $F=71$ witnesses whose backward trees may continue.
3. **Forward record search.** Evaluate new starting values with memoized trajectories and exact factorization.
4. **Hybrid meet-in-the-middle search.** Build backward basin fragments and connect them to forward trajectories.
5. **Structural arithmetic search.** Use factorization constraints on $\varphi(n)$, admissible primes $p$ with $p-1\mid m$, and controlled prime-power products.

## Acceptance contract for a new record

A claimed witness for $F=r$ is accepted only when the packet contains:

- the complete $r+1$-node trajectory;
- proof that every earlier node is composite;
- proof that the terminal node is prime;
- exact factorizations and totients for every transition;
- at least one package-free verifier;
- an independent implementation or reconstruction;
- a cryptographic manifest;
- explicit statements of what the result does and does not prove.

## Research ledger

Every attempted lane should record one of:

- `CERTIFIED_RECORD`;
- `CERTIFIED_LOCAL_EXHAUSTION`;
- `CANDIDATE_REJECTED` with reason;
- `INCOMPLETE_SEARCH` with exact restart boundary;
- `HEURISTIC_ONLY`;
- `ENVIRONMENT_LIMIT`.

A local exhaustion statement must identify its root set, search universe, algorithm, and completeness argument.
