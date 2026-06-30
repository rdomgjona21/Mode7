import csv
from pathlib import Path

import numpy as np

from aetherfront.audio.manager import (
    MUSIC_FILES,
    MUSIC_VOLUME,
    SFX_FILES,
    SFX_MAXTIME_MS,
    SFX_VOLUME,
    AudioManager,
    MusicTrack,
    SoundEffect,
    _music_array,
    audio_asset_paths,
    music_asset_paths,
)


def test_all_declared_sound_effect_assets_exist() -> None:
    paths = audio_asset_paths()

    assert set(paths) == set(SoundEffect)
    for effect, path in paths.items():
        assert path.exists(), effect
        assert path.suffix == ".mp3"
        assert path.stat().st_size > 0


def test_sound_effect_files_use_stable_lowercase_names() -> None:
    for filename in SFX_FILES.values():
        assert filename == filename.lower()
        assert " " not in filename
        assert "#" not in filename


def test_all_declared_music_assets_exist() -> None:
    paths = music_asset_paths()

    assert set(paths) == set(MusicTrack)
    for track, path in paths.items():
        assert path.exists(), track
        assert path.suffix == ".wav"
        assert path.stat().st_size > 0


def test_music_files_use_stable_lowercase_names() -> None:
    for filename in MUSIC_FILES.values():
        assert filename == filename.lower()
        assert " " not in filename
        assert "#" not in filename


def test_sound_effect_manifest_contains_every_audio_asset() -> None:
    manifest_path = Path("src/aetherfront/assets/manifest.csv")
    with manifest_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    manifest_paths = {row["path"] for row in rows}
    for filename in SFX_FILES.values():
        assert f"assets/audio/sfx/{filename}" in manifest_paths
    for filename in MUSIC_FILES.values():
        assert f"assets/audio/music/{filename}" in manifest_paths


def test_documented_asset_licenses_contain_every_audio_asset() -> None:
    manifest_path = Path("docs/asset-licenses.csv")
    with manifest_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    manifest_paths = {row["path"] for row in rows}
    for filename in SFX_FILES.values():
        assert f"src/aetherfront/assets/audio/sfx/{filename}" in manifest_paths
    for filename in MUSIC_FILES.values():
        assert f"src/aetherfront/assets/audio/music/{filename}" in manifest_paths


def test_audio_manager_disabled_mode_is_safe() -> None:
    manager = AudioManager.disabled()

    for effect in SoundEffect:
        manager.play(effect)
        manager.play_terminal(effect)
    for track in MusicTrack:
        manager.play_music(track)
    manager.stop_music()

    assert not manager.enabled


def test_sound_effect_volumes_and_playback_caps_are_valid() -> None:
    assert set(SFX_VOLUME) == set(SoundEffect)
    for volume in SFX_VOLUME.values():
        assert 0.0 <= volume <= 1.0
    for effect, maxtime in SFX_MAXTIME_MS.items():
        assert effect in SoundEffect
        assert maxtime > 0


def test_music_volumes_are_defined_for_every_track() -> None:
    assert set(MUSIC_VOLUME) == set(MusicTrack)
    for volume in MUSIC_VOLUME.values():
        assert 0.0 <= volume <= 1.0


def test_repeated_combat_sfx_are_quieter_than_music() -> None:
    repeated_effects = {
        SoundEffect.CANNON_FIRE,
        SoundEffect.SPREAD_FIRE,
        SoundEffect.ENEMY_LIGHT_FIRE,
        SoundEffect.ENEMY_HEAVY_FIRE,
        SoundEffect.BOSS_HIT,
    }

    assert max(SFX_VOLUME[effect] for effect in repeated_effects) < min(MUSIC_VOLUME.values())


def test_music_tracks_generate_stereo_int16_audio() -> None:
    for track in MusicTrack:
        audio = _music_array(track, sample_rate=8000)
        assert audio.dtype == np.int16
        assert audio.shape == (64000, 2)
        assert np.any(audio)
        assert np.max(np.abs(audio)) > 7_000
