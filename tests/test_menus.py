import numpy as np
import pygame

from aetherfront.config import INTERNAL_SIZE
from aetherfront.gameplay.session import CombatSession
from aetherfront.rendering.camera import Camera
from aetherfront.ui.menus import (
    draw_instructions,
    draw_main_menu,
    draw_pause_menu,
    draw_terminal_menu,
)


def _non_empty_after_draw(draw_call) -> bool:  # type: ignore[no-untyped-def]
    pygame.font.init()
    try:
        canvas = pygame.Surface(INTERNAL_SIZE)
        font = pygame.font.Font(None, 26)
        draw_call(canvas, font)
        return bool(np.any(pygame.surfarray.array3d(canvas) != 0))
    finally:
        pygame.font.quit()


def test_main_menu_draws_visible_pixels_headless() -> None:
    assert _non_empty_after_draw(draw_main_menu)


def test_instructions_draw_visible_pixels_headless() -> None:
    assert _non_empty_after_draw(draw_instructions)


def test_pause_menu_draws_visible_pixels_headless() -> None:
    assert _non_empty_after_draw(draw_pause_menu)


def test_terminal_menu_draws_only_after_terminal_state() -> None:
    session = CombatSession.create(Camera())

    assert not _non_empty_after_draw(lambda canvas, font: draw_terminal_menu(canvas, font, session))

    session.victory = True
    assert _non_empty_after_draw(lambda canvas, font: draw_terminal_menu(canvas, font, session))
