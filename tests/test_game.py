import pygame
import pytest

from aetherfront.core.game import Game


def test_game_runs_one_headless_frame(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")

    assert Game().run(max_frames=1) == 0
    assert not pygame.get_init()


def test_game_rejects_invalid_frame_limit() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        Game().run(max_frames=0)
