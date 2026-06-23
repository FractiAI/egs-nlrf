#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
pip install -q -r requirements_lock.txt
export PYTHONPATH="$(pwd)/src/python"
python tools/fetch_hydrogen_data.py
python tools/verify_audit.py
echo "=== EGS-NLRF PIPELINE COMPLETE ==="
