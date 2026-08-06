#!/usr/bin/env python3
"""Verify every file listed in SHA256SUMS."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256SUMS"


def main() -> None:
    checked = 0
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        digest, rel = raw.split("  ", 1)
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            raise AssertionError(f"SHA-256 mismatch for {rel}: {actual} != {digest}")
        checked += 1
    print(f"VERIFIED: {checked} SHA-256 manifest entries.")


if __name__ == "__main__":
    main()
