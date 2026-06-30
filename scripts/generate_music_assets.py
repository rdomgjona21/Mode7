"""Generate deterministic WAV music loops for Aetherfront."""

from __future__ import annotations

import wave
from pathlib import Path

from aetherfront.audio.manager import MUSIC_FILES, MusicTrack, _music_array

SAMPLE_RATE = 44_100
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "src/aetherfront/assets/audio/music"


def write_wave(path: Path, audio) -> None:
    """Write a stereo int16 NumPy array as a PCM WAV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(audio.tobytes())


def main() -> int:
    """Regenerate all packaged music loops."""
    for track in MusicTrack:
        write_wave(OUTPUT_DIR / MUSIC_FILES[track], _music_array(track, SAMPLE_RATE))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
