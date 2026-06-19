#!/usr/bin/env bash
set -euo pipefail

python -m ruff check . --no-cache
python -m pytest
