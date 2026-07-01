from types import SimpleNamespace

import pygame
import pytest

from aetherfront.audio.manager import MusicTrack, SoundEffect
from aetherfront.core.game import Game, GameRuntimeState
from aetherfront.core.states import AppState
from aetherfront.gameplay.weapons import PrimaryWeapon


class StubAudio:
    """Minimalni audio double za testiranje state handlera bez PyGame mixera."""

    def __init__(self) -> None:
        self.played: list[SoundEffect] = []
        self.stopped_music = 0

    def play(self, effect: SoundEffect) -> None:
        self.played.append(effect)

    def stop_music(self) -> None:
        self.stopped_music += 1


def _event(key: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=key)


def _runtime_state(app_state: AppState = AppState.MAIN_MENU) -> GameRuntimeState:
    camera, session = Game._new_attempt()
    return GameRuntimeState(app_state=app_state, camera=camera, session=session)


def test_control_axis_combines_opposite_keys() -> None:
    """Jedna tipka daje puni smjer, a dvije suprotne tipke daju neutralni ulaz."""
    assert Game._axis(positive=True, negative=False) == 1.0
    assert Game._axis(positive=False, negative=True) == -1.0
    assert Game._axis(positive=True, negative=True) == 0.0


def test_game_runs_one_headless_frame(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pokreni jedan frame bez otvaranja stvarnog prozora ili zvučnog uređaja."""
    # Dummy SDL upravljački programi omogućuju izvođenje testa i bez grafičkog okruženja.
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")

    # Nakon izvođenja provjeravamo i rezultat i uredno gašenje svih PyGame modula.
    assert Game().run(max_frames=1) == 0
    assert not pygame.get_init()


def test_game_rejects_invalid_frame_limit() -> None:
    """Nula frameova nema smisla i mora proizvesti jasno objašnjenu pogrešku."""
    with pytest.raises(ValueError, match="at least 1"):
        Game().run(max_frames=0)


def test_music_for_session_falls_back_when_wave_number_is_unexpected() -> None:
    """Neispravan broj vala ne smije rušiti audio odabir KeyErrorom."""
    session = SimpleNamespace(
        boss=None,
        wave_director=SimpleNamespace(current_wave_number=99),
    )

    assert Game._music_for_session(session) is MusicTrack.WAVE_1


def test_menu_enter_starts_playing_attempt() -> None:
    state = _runtime_state()
    original_session = state.session
    audio = StubAudio()

    Game._handle_menu_event(_event(pygame.K_RETURN), state, audio)  # type: ignore[arg-type]

    assert state.app_state is AppState.PLAYING
    assert state.session is not original_session
    assert audio.played == [SoundEffect.MENU_SELECT]


def test_menu_can_open_instructions_and_escape_can_quit() -> None:
    state = _runtime_state()
    audio = StubAudio()

    Game._handle_menu_event(_event(pygame.K_i), state, audio)  # type: ignore[arg-type]
    assert state.app_state is AppState.INSTRUCTIONS
    assert state.running

    Game._handle_menu_event(_event(pygame.K_ESCAPE), state, audio)  # type: ignore[arg-type]
    assert not state.running


def test_instructions_can_start_or_return_to_menu() -> None:
    state = _runtime_state(AppState.INSTRUCTIONS)
    audio = StubAudio()

    Game._handle_instructions_event(_event(pygame.K_m), state, audio)  # type: ignore[arg-type]
    assert state.app_state is AppState.MAIN_MENU

    state.app_state = AppState.INSTRUCTIONS
    Game._handle_instructions_event(_event(pygame.K_SPACE), state, audio)  # type: ignore[arg-type]
    assert state.app_state is AppState.PLAYING


def test_playing_escape_pauses_and_pause_escape_resumes() -> None:
    state = _runtime_state(AppState.PLAYING)
    audio = StubAudio()

    Game._handle_game_event(_event(pygame.K_ESCAPE), state, audio)  # type: ignore[arg-type]
    assert state.app_state is AppState.PAUSED
    assert audio.played == [SoundEffect.PAUSE]
    assert audio.stopped_music == 1

    Game._handle_pause_event(_event(pygame.K_ESCAPE), state, audio)  # type: ignore[arg-type]
    assert state.app_state is AppState.PLAYING
    assert audio.played == [SoundEffect.PAUSE, SoundEffect.PAUSE]
    assert audio.stopped_music == 2


def test_terminal_menu_return_resets_attempt_and_stops_music() -> None:
    state = _runtime_state(AppState.PLAYING)
    original_session = state.session
    state.session.victory = True
    state.terminal_audio_played = "victory"
    audio = StubAudio()

    Game._handle_game_event(_event(pygame.K_m), state, audio)  # type: ignore[arg-type]

    assert state.app_state is AppState.MAIN_MENU
    assert state.session is not original_session
    assert state.terminal_audio_played is None
    assert audio.played == [SoundEffect.MENU_SELECT]
    assert audio.stopped_music == 1


def test_game_event_changes_primary_weapon_with_ready_sound() -> None:
    state = _runtime_state(AppState.PLAYING)
    audio = StubAudio()

    Game._handle_game_event(_event(pygame.K_2), state, audio)  # type: ignore[arg-type]

    assert state.session.weapons.primary is PrimaryWeapon.SPREAD
    assert audio.played == [SoundEffect.WEAPON_READY]
