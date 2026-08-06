# Data reference

## `trajectory_certificate.json.gz`

Schema: `erdos409-trajectory-certificate-v2`

Contains:

- the claim $F(6{,}668{,}696{,}999)=71$;
- the nested $F=68,69,70,71$ witnesses;
- all 72 ordered nodes;
- complete factorizations of all 71 composite nodes;
- exact totients and next values;
- the terminal prime.

## `prime_certificates.json.gz`

Schema: `lucas-pratt-prime-certificates-v2`

Contains 222 recursively dependent primality certificates. For each $p>2$, the packet gives a complete factorization of $p-1$ and a Lucas witness.

## `inverse_totient_tree.json.gz`

Schema: `erdos409-inverse-totient-tree-v1`

Contains the exact rooted levels $F=68$ through the attempted direct $F=72$ extension, plus all parent-child edges satisfying

$$
\varphi(\text{child})+1=\text{parent}.
$$

## Flat formats

- `trajectory.csv`: index, value, status, factorization, totient, next value.
- `trajectory.txt`: one trajectory value per line.
- `inverse_tree_nodes.csv`: every rooted value with its level, factorization, and parent count.
- `inverse_tree_edges.csv`: one rooted inverse-tree edge per row.
- `record_chain.csv`: the certified $F=68$ through $F=71$ progression.
- `summary.json`: concise counts and record-chain metadata.

The gzip files are deterministic: the timestamp is fixed to zero, and the JSON is serialized with sorted keys and compact separators.
