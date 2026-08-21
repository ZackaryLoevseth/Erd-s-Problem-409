# Certificate packet for an F = 104 witness

This self-contained packet verifies `F(400000287233629) = 104` for
`T(n) = phi(n) + 1`, stopping at the first prime.

- Witness: `400000287233629`
- Terminal prime: `27515203921`
- Trajectory nodes: `105`
- Canonical trajectory SHA-256: `3faf8aa1b74ffa39d8e72b45b0a57ceffbc631a958f7a8bed758d3caaa745394`

Run `bash run_all.sh`, or invoke `verify.py` with SymPy and then invoke the
dependency-free `verify_independent.py`. The two evaluators use structurally
different factorization, primality, and totient implementations.

This packet certifies one pointwise value. Search coverage, inverse-enumeration
completeness, novelty, and the general questions in Erdős Problem #409 are
separate claims.
