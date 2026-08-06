# Historical packet hashes and availability qualification

The July 2026 README recorded a larger 118-entry certificate archive with the following hashes.

## Historical archive SHA-256

```text
ca5b9a9e69f9a91e3de2642452259c307a416f659349c5067cb20c692f42d026
```

## Historical canonical-trajectory SHA-256

```text
6a6758b8bb6e2d2cd812301b04eabc9d14699d18908a1cdf7066454934802ad7
```

These values are preserved as provenance. They are not the hashes of the reconstructed files in the present repository.

During the August 2026 migration audit, no corresponding release asset was present in the accessible renamed repository. Therefore the current publication:

- does not claim byte identity with the unavailable archive;
- reconstructs and verifies the arithmetic directly;
- publishes a new deterministic certificate packet;
- records new hashes in [`../SHA256SUMS`](../SHA256SUMS);
- distinguishes historical availability claims from current accessible artifacts.
