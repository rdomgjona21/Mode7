import numpy as np
import pygame

from aetherfront.config import INTERNAL_SIZE
from aetherfront.gameplay.session import CombatSession
from aetherfront.rendering.camera import Camera
from aetherfront.ui.hud import draw_hud


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
        assert np.any(pixels[:252, :150] != 0)
        assert np.all(pixels[280, 170] == 0)
    finally:
        pygame.font.quit()
