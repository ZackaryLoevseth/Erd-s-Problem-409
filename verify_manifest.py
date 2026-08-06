#!/usr/bin/env python3
"""Verify all SHA-256 entries listed in SHA256SUMS."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256SUMS"


def main() -> None:
    checked = 0
    for line_number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            expected, relative = line.split("  ", 1)
        except ValueError as exc:
            raise RuntimeError(f"Malformed manifest line {line_number}") from exc

        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"Missing manifest file: {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(
                f"SHA-256 mismatch for {relative}: expected {expected}, got {actual}"
            )
        checked += 1

    print(f"VERIFIED: {checked} SHA-256 manifest entries.")


if __name__ == "__main__":
    main()
