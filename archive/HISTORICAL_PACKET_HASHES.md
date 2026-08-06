# Historical packet hashes and migration record

The earlier July 2026 README recorded the following hashes for a larger certificate packet:

## Historical archive SHA-256

```text
ca5b9a9e69f9a91e3de2642452259c307a416f659349c5067cb20c692f42d026
```

## Historical canonical-trajectory SHA-256

```text
6a6758b8bb6e2d2cd812301b04eabc9d14699d18908a1cdf7066454934802ad7
```

These values are preserved as provenance. They are **not** the hashes of the reconstructed files in this repository.

The earlier README stated that the complete archive was available through GitHub Releases. During the August 2026 migration audit, no release asset was present on the renamed repository. Accordingly:

- this repository does not claim byte identity with that unavailable archive;
- the new public packet is independently regenerated from the stated witness;
- the new packet has its own hashes in [`../SHA256SUMS`](../SHA256SUMS);
- the mathematical result is checked directly rather than inferred from the historical hashes.

## Source Git history

The earlier #409 public tree survives in the history of the repository later renamed for Problem #64:

```text
commit 905b682406251e98c9a2d1569a8a67ae82910a0e
tree   3fbb30d9ede96e07e88b463654ce1e7c21afb88d
```

The old tree contained six files: `AI_USAGE.md`, `CITATION.cff`, `LICENSE`, `README.md`, `requirements.txt`, and `verify.py`.
