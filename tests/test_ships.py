import numpy as np
import pygame

from aetherfront.config import PLAYER_SURFACE_SIZE
from aetherfront.rendering.ships import create_kestrel_surface


def test_kestrel_has_expected_size_and_transparency() -> None:
    surface = create_kestrel_surface()

    assert surface.get_size() == PLAYER_SURFACE_SIZE
    assert surface.get_flags() & pygame.SRCALPHA


def test_kestrel_contains_visible_and_transparent_pixels() -> None:
    surface = create_kestrel_surface()
    alpha = pygame.surfarray.array_alpha(surface)
    colors = pygame.surfarray.array3d(surface)

    assert np.any(alpha == 0)
    assert np.any(alpha > 0)
    assert np.unique(colors[alpha > 0], axis=0).shape[0] > 4
