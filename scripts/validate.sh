#!/usr/bin/env bash
# Prekini skriptu nakon prve pogreške, nedostajuće varijable ili neuspjele pipe naredbe.
set -euo pipefail

# Ruff provjerava stil i česte pogreške, a Pytest zatim izvodi automatizirane testove.
python -m ruff check . --no-cache
python -m pytest
