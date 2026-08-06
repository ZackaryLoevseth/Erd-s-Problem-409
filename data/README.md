# Data files

## `certificate.json.gz`

Schema: `erdos409-trajectory-certificate-v1`

The file contains 69 ordered nodes. Each composite node records:

- its index;
- the integer \(n\);
- its complete prime factorization;
- \(\varphi(n)\);
- the next value \(\varphi(n)+1\).

The final node records the terminal prime.

## `prime_certificates.json.gz`

Schema: `lucas-pratt-prime-certificates-v1`

For every prime appearing in the trajectory factorizations, and recursively for the primes needed to certify those primes, the file records:

- a complete factorization of \(p-1\);
- a witness \(a\);
- recursive dependencies.

For \(p>2\), the checker verifies

\[
a^{p-1}\equiv1\pmod p
\]

and, for every prime \(q\mid p-1\),

\[
\gcd\!\left(a^{(p-1)/q}-1,p\right)=1.
\]

Together with the certified complete factorization of \(p-1\), these Lucas conditions prove that \(p\) is prime.

## `trajectory.csv`

A human- and spreadsheet-readable table with columns:

`index,n,status,factorization,phi,next`

## `trajectory.txt`

The 69 trajectory values, one decimal integer per line. This is the simplest canonical representation of the reconstructed orbit.

Both JSON files are gzip-compressed deterministically. Use `gzip -dc FILE.json.gz` to inspect their UTF-8 JSON contents.
