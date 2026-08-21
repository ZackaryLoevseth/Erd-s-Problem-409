#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install -r requirements.txt
python3 verify.py
python3 verify_independent.py
shasum -a 256 -c MANIFEST.sha256
