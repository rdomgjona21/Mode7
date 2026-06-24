import numpy as np
import pygame

from aetherfront.config import INTERNAL_SIZE
from aetherfront.gameplay.session import CombatSession
from aetherfront.rendering.camera import Camera
from aetherfront.ui.hud import draw_hud, format_elapsed_time


def test_elapsed_time_formats_as_minutes_and_seconds() -> None:
    assert format_elapsed_time(0) == "00:00"
    assert format_elapsed_time(74.9) == "01:14"
    assert format_elapsed_time(-5) == "00:00"


def test_hud_draws_visible_pixels_headless() -> None:
    pygame.font.init()
    try:
        canvas = pygame.Surface(INTERNAL_SIZE)
        font = pygame.font.Font(None, 20)
        draw_hud(canvas, font, CombatSession.create(Camera()), speed=20, fps=60)

        assert np.any(pygame.surfarray.array3d(canvas) != 0)
    finally:
        pygame.font.quit()


def test_hud_uses_compact_left_panel() -> None:
    pygame.font.init()
    try:
        canvas = pygame.Surface(INTERNAL_SIZE)
        font = pygame.font.Font(None, 20)
        draw_hud(canvas, font, CombatSession.create(Camera()), speed=20, fps=60)

        pixels = pygame.surfarray.array3d(canvas)
        assert np.any(pixels[:252, :164] != 0)
        assert np.all(pixels[280, 180] == 0)
    finally:
        pygame.font.quit()
