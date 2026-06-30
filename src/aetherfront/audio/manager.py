"""PyGame mixer wrapper for ElevenLabs sound effects and procedural music."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import StrEnum
from importlib.resources import files
from pathlib import Path
from typing import Final

import numpy as np
import pygame


class SoundEffect(StrEnum):
    """Stable identifiers for all gameplay and UI sound effects."""

    CANNON_FIRE = "cannon_fire"
    SPREAD_FIRE = "spread_fire"
    ROCKET_LAUNCH = "rocket_launch"
    ENEMY_LIGHT_FIRE = "enemy_light_fire"
    ENEMY_HEAVY_FIRE = "enemy_heavy_fire"
    ENEMY_DESTROYED = "enemy_destroyed"
    BOSS_HIT = "boss_hit"
    BOSS_DESTROYED = "boss_destroyed"
    REPAIR_PICKUP = "repair_pickup"
    PLAYER_DAMAGE = "player_damage"
    WEAPON_READY = "weapon_ready"
    WAVE_START = "wave_start"
    BOSS_ARRIVAL = "boss_arrival"
    MENU_SELECT = "menu_select"
    PAUSE = "pause"
    VICTORY = "victory"
    GAME_OVER = "game_over"


class MusicTrack(StrEnum):
    """Looping procedural music layers for combat progression."""

    MENU = "menu"
    WAVE_1 = "wave_1"
    WAVE_2 = "wave_2"
    WAVE_3 = "wave_3"
    BOSS_PHASE_1 = "boss_phase_1"
    BOSS_PHASE_2 = "boss_phase_2"


SFX_FILES: Final[dict[SoundEffect, str]] = {
    # Ova mapa je jedino mjesto gdje se logički naziv efekta povezuje s MP3 datotekom.
    # Ostatak igre koristi `SoundEffect`, pa promjena imena datoteke ne dira gameplay kod.
    SoundEffect.CANNON_FIRE: "cannon_fire.mp3",
    SoundEffect.SPREAD_FIRE: "spread_fire.mp3",
    SoundEffect.ROCKET_LAUNCH: "rocket_launch.mp3",
    SoundEffect.ENEMY_LIGHT_FIRE: "enemy_light_fire.mp3",
    SoundEffect.ENEMY_HEAVY_FIRE: "enemy_heavy_fire.mp3",
    SoundEffect.ENEMY_DESTROYED: "enemy_destroyed.mp3",
    SoundEffect.BOSS_HIT: "boss_hit.mp3",
    SoundEffect.BOSS_DESTROYED: "boss_destroyed.mp3",
    SoundEffect.REPAIR_PICKUP: "repair_pickup.mp3",
    SoundEffect.PLAYER_DAMAGE: "player_damage.mp3",
    SoundEffect.WEAPON_READY: "weapon_ready.mp3",
    SoundEffect.WAVE_START: "wave_start.mp3",
    SoundEffect.BOSS_ARRIVAL: "boss_arrival.mp3",
    SoundEffect.MENU_SELECT: "menu_select.mp3",
    SoundEffect.PAUSE: "pause.mp3",
    SoundEffect.VICTORY: "victory.mp3",
    SoundEffect.GAME_OVER: "game_over.mp3",
}

MUSIC_FILES: Final[dict[MusicTrack, str]] = {
    # Glazba je odvojena od SFX-a jer se reproducira kao loop na rezerviranom kanalu.
    MusicTrack.MENU: "menu.wav",
    MusicTrack.WAVE_1: "wave_1.wav",
    MusicTrack.WAVE_2: "wave_2.wav",
    MusicTrack.WAVE_3: "wave_3.wav",
    MusicTrack.BOSS_PHASE_1: "boss_phase_1.wav",
    MusicTrack.BOSS_PHASE_2: "boss_phase_2.wav",
}

SFX_VOLUME: Final[dict[SoundEffect, float]] = {
    # Borbeni SFX-ovi su namjerno tihi da ne pregaze glazbu. Glasniji su samo rijetki
    # događaji poput pobjede, poraza i uništenja bossa.
    SoundEffect.CANNON_FIRE: 0.10,
    SoundEffect.SPREAD_FIRE: 0.09,
    SoundEffect.ROCKET_LAUNCH: 0.14,
    SoundEffect.ENEMY_LIGHT_FIRE: 0.05,
    SoundEffect.ENEMY_HEAVY_FIRE: 0.08,
    SoundEffect.ENEMY_DESTROYED: 0.16,
    SoundEffect.BOSS_HIT: 0.12,
    SoundEffect.BOSS_DESTROYED: 0.24,
    SoundEffect.REPAIR_PICKUP: 0.14,
    SoundEffect.PLAYER_DAMAGE: 0.16,
    SoundEffect.WEAPON_READY: 0.09,
    SoundEffect.WAVE_START: 0.16,
    SoundEffect.BOSS_ARRIVAL: 0.20,
    SoundEffect.MENU_SELECT: 0.10,
    SoundEffect.PAUSE: 0.10,
    SoundEffect.VICTORY: 0.34,
    SoundEffect.GAME_OVER: 0.32,
}

SFX_MAXTIME_MS: Final[dict[SoundEffect, int]] = {
    # Dulji izvori se režu kako kratki gameplay događaj ne bi nastavio zvučati predugo.
    SoundEffect.ENEMY_LIGHT_FIRE: 700,
    SoundEffect.WEAPON_READY: 650,
}

MUSIC_VOLUME: Final[dict[MusicTrack, float]] = {
    # Loopovi postaju malo glasniji kako misija raste prema boss fazi.
    MusicTrack.MENU: 0.50,
    MusicTrack.WAVE_1: 0.58,
    MusicTrack.WAVE_2: 0.62,
    MusicTrack.WAVE_3: 0.66,
    MusicTrack.BOSS_PHASE_1: 0.70,
    MusicTrack.BOSS_PHASE_2: 0.76,
}

MUSIC_CHANNEL_INDEX: Final = 0
MUSIC_LOOP_SECONDS: Final = 8.0


@dataclass(slots=True)
class AudioManager:
    """Load and play short sound effects while tolerating missing audio devices."""

    enabled: bool = True
    sounds: dict[SoundEffect, pygame.mixer.Sound] = field(default_factory=dict)
    music: dict[MusicTrack, pygame.mixer.Sound] = field(default_factory=dict)
    music_channel: pygame.mixer.Channel | None = None
    current_music: MusicTrack | None = None

    @classmethod
    def load(cls) -> AudioManager:
        """Create an audio manager from packaged MP3 assets."""
        try:
            # Mixer se inicijalizira ovdje, a ne u glavnoj petlji, da cijeli audio sloj
            # može prijeći u no-op način ako macOS ili headless test nema audio uređaj.
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except pygame.error:
            return cls.disabled()

        # Kanal 0 rezerviran je za glazbu; preostali kanali ostaju dostupni za SFX.
        pygame.mixer.set_num_channels(max(16, pygame.mixer.get_num_channels()))
        pygame.mixer.set_reserved(1)
        manager = cls(enabled=True, music_channel=pygame.mixer.Channel(MUSIC_CHANNEL_INDEX))
        sfx_root = files("aetherfront").joinpath("assets/audio/sfx")
        for effect, filename in SFX_FILES.items():
            # Nedostajući pojedinačni asset ne ruši igru. Efekt se samo preskoči, a
            # package/test skripte zasebno provjeravaju da produkcijski asseti postoje.
            try:
                sound = pygame.mixer.Sound(str(sfx_root.joinpath(filename)))
            except (FileNotFoundError, pygame.error):
                continue
            sound.set_volume(SFX_VOLUME[effect])
            manager.sounds[effect] = sound
        music_root = files("aetherfront").joinpath("assets/audio/music")
        for track, filename in MUSIC_FILES.items():
            # Music trackovi se učitavaju kao Sound objekti jer PyGame mixer music API
            # koristi jedan globalni stream, a nama treba kontrolirani rezervirani kanal.
            try:
                sound = pygame.mixer.Sound(str(music_root.joinpath(filename)))
            except (FileNotFoundError, pygame.error):
                continue
            manager.music[track] = sound
        for track, sound in manager.music.items():
            sound.set_volume(MUSIC_VOLUME[track])
        if not manager.sounds:
            return cls.disabled()
        return manager

    @classmethod
    def disabled(cls) -> AudioManager:
        """Return a no-op manager used when audio cannot be initialized."""
        return cls(enabled=False)

    def play(self, effect: SoundEffect) -> None:
        """Play one sound effect if audio is available and the asset was loaded."""
        if not self.enabled:
            return
        sound = self.sounds.get(effect)
        if sound is None:
            return
        try:
            # `maxtime=0` znači pusti cijeli efekt; za problematično duge efekte koristi
            # se vrijednost iz `SFX_MAXTIME_MS`.
            sound.play(maxtime=SFX_MAXTIME_MS.get(effect, 0))
        except pygame.error:
            self.enabled = False

    def play_terminal(self, effect: SoundEffect) -> None:
        """Stop overlapping effects and play a high-priority terminal sound."""
        if not self.enabled:
            return
        try:
            # Pobjeda i poraz trebaju biti jasni, zato se prije njih gase preostali
            # kratki efekti i glazba.
            pygame.mixer.stop()
            self.current_music = None
        except pygame.error:
            self.enabled = False
            return
        self.play(effect)

    def play_music(self, track: MusicTrack) -> None:
        """Loop the requested music track unless it is already active."""
        if not self.enabled or self.music_channel is None:
            return
        if self.current_music is track and self.music_channel.get_busy():
            return
        sound = self.music.get(track)
        if sound is None:
            return
        try:
            # Promjena vala ili boss faze zamjenjuje loop kratkim fadeom da prijelaz ne
            # zvuči kao nagli rez.
            self.music_channel.stop()
            self.music_channel.play(sound, loops=-1, fade_ms=250)
            self.current_music = track
        except pygame.error:
            self.enabled = False

    def stop_music(self) -> None:
        """Fade out the active music loop."""
        if not self.enabled or self.music_channel is None or self.current_music is None:
            return
        try:
            self.music_channel.fadeout(350)
            self.current_music = None
        except pygame.error:
            self.enabled = False


def audio_asset_paths() -> dict[SoundEffect, Path]:
    """Return local source-tree paths for tests and manifest validation."""
    root = Path(__file__).resolve().parents[1] / "assets" / "audio" / "sfx"
    return {effect: root / filename for effect, filename in SFX_FILES.items()}


def music_asset_paths() -> dict[MusicTrack, Path]:
    """Return local source-tree paths for generated music assets."""
    root = Path(__file__).resolve().parents[1] / "assets" / "audio" / "music"
    return {track: root / filename for track, filename in MUSIC_FILES.items()}


def _create_music_bank() -> dict[MusicTrack, pygame.mixer.Sound]:
    sample_rate = pygame.mixer.get_init()[0]
    return {
        track: pygame.sndarray.make_sound(_music_array(track, sample_rate))
        for track in MusicTrack
    }


def _music_array(track: MusicTrack, sample_rate: int) -> np.ndarray:
    specs: dict[MusicTrack, tuple[float, float, tuple[int, ...], float]] = {
        MusicTrack.MENU: (76.0, 116.54, (0, 3, 7, 10), 0.24),
        MusicTrack.WAVE_1: (92.0, 130.81, (0, 3, 5, 7), 0.34),
        MusicTrack.WAVE_2: (108.0, 146.83, (0, 3, 7, 10), 0.42),
        MusicTrack.WAVE_3: (126.0, 164.81, (0, 5, 7, 12), 0.50),
        MusicTrack.BOSS_PHASE_1: (104.0, 87.31, (0, 3, 6, 7), 0.55),
        MusicTrack.BOSS_PHASE_2: (138.0, 92.50, (0, 3, 6, 10), 0.64),
    }
    tempo, root, pattern, intensity = specs[track]
    sample_count = int(sample_rate * MUSIC_LOOP_SECONDS)
    time = np.arange(sample_count, dtype=np.float32) / sample_rate
    beat_seconds = 60.0 / tempo
    beat_phase = np.mod(time, beat_seconds) / beat_seconds

    drone = np.sin(math.tau * root * 0.5 * time) * 0.22
    engine = np.sin(
        math.tau * (root * 0.25 + np.sin(math.tau * 0.5 * time) * 1.6) * time
    ) * 0.16
    pulse = np.exp(-beat_phase * 10.0) * np.sin(math.tau * root * time) * intensity
    tick_gate = (beat_phase < 0.08).astype(np.float32)
    tick = tick_gate * np.sin(math.tau * root * 4.0 * time) * (0.08 + intensity * 0.08)

    melody = np.zeros_like(time)
    half_beat = beat_seconds * 0.5
    note_index = np.floor(time / half_beat).astype(np.int32) % len(pattern)
    note_phase = np.mod(time, half_beat) / half_beat
    envelope = np.exp(-note_phase * 5.0)
    for index, semitone in enumerate(pattern):
        mask = note_index == index
        frequency = root * (2.0 ** (semitone / 12.0))
        melody[mask] = np.sin(math.tau * frequency * time[mask]) * envelope[mask] * 0.16

    if track is MusicTrack.BOSS_PHASE_2:
        pulse += np.sin(math.tau * root * 1.5 * time) * np.exp(-beat_phase * 14.0) * 0.20
    elif track is MusicTrack.BOSS_PHASE_1:
        drone += np.sin(math.tau * root * 0.75 * time) * 0.14
    elif track is MusicTrack.MENU:
        pulse *= 0.45
        tick *= 0.35
        drone += np.sin(math.tau * root * 0.25 * time) * 0.10

    mono = (drone + engine + pulse + tick + melody) * 0.52
    mono = np.tanh(mono)
    pan = np.sin(math.tau * time / MUSIC_LOOP_SECONDS) * 0.08
    left = mono * (1.0 - pan)
    right = mono * (1.0 + pan)
    stereo = np.column_stack((left, right))
    return np.asarray(stereo * 32767, dtype=np.int16)
