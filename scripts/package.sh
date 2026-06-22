#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"
export PYINSTALLER_CONFIG_DIR="$project_root/tmp/pyinstaller"

./scripts/validate.sh

python -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name Aetherfront \
  --osx-bundle-identifier hr.foi.aetherfront \
  --collect-data aetherfront \
  --paths src \
  src/aetherfront/main.py

executable="dist/Aetherfront.app/Contents/MacOS/Aetherfront"
if [[ ! -x "$executable" ]]; then
  echo "Packaging failed: expected executable is missing: $executable" >&2
  exit 1
fi

balance_file="$(find dist/Aetherfront.app -path '*/aetherfront/data/balance.json' -print -quit)"
if [[ -z "$balance_file" ]]; then
  echo "Packaging failed: balance.json is missing from the application bundle" >&2
  exit 1
fi

echo "Created dist/Aetherfront.app"
