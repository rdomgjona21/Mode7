import pygame
import pytest

from aetherfront.core.game import Game


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
