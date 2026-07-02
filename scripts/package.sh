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

waves_file="$(find dist/Aetherfront.app -path '*/aetherfront/data/waves.json' -print -quit)"
if [[ -z "$waves_file" ]]; then
  echo "Packaging failed: waves.json is missing from the application bundle" >&2
  exit 1
fi

sfx_file="$(find dist/Aetherfront.app -path '*/aetherfront/assets/audio/sfx/cannon_fire.mp3' -print -quit)"
if [[ -z "$sfx_file" ]]; then
  echo "Packaging failed: sound effects are missing from the application bundle" >&2
  exit 1
fi

music_file="$(find dist/Aetherfront.app -path '*/aetherfront/assets/audio/music/wave_1.wav' -print -quit)"
if [[ -z "$music_file" ]]; then
  echo "Packaging failed: music loops are missing from the application bundle" >&2
  exit 1
fi

menu_music_file="$(find dist/Aetherfront.app -path '*/aetherfront/assets/audio/music/menu.wav' -print -quit)"
if [[ -z "$menu_music_file" ]]; then
  echo "Packaging failed: menu music is missing from the application bundle" >&2
  exit 1
fi

cloud_texture_file="$(find dist/Aetherfront.app -path '*/aetherfront/assets/images/terrain/cloud_layer.png' -print -quit)"
if [[ -z "$cloud_texture_file" ]]; then
  echo "Packaging failed: cloud terrain texture is missing from the application bundle" >&2
  exit 1
fi

zip_file="dist/Aetherfront-Zeppelin-Wars-macOS.zip"
rm -f "$zip_file"
ditto -c -k --keepParent dist/Aetherfront.app "$zip_file"
if [[ ! -s "$zip_file" ]]; then
  echo "Packaging failed: expected release ZIP is missing or empty: $zip_file" >&2
  exit 1
fi

zip_smoke_dir="$(mktemp -d "${TMPDIR:-/tmp}/aetherfront_zip_smoke.XXXXXX")"
ditto -x -k "$zip_file" "$zip_smoke_dir"
if [[ ! -x "$zip_smoke_dir/Aetherfront.app/Contents/MacOS/Aetherfront" ]]; then
  echo "Packaging failed: extracted ZIP does not contain a runnable app" >&2
  exit 1
fi

echo "Created dist/Aetherfront.app"
echo "Created $zip_file"
