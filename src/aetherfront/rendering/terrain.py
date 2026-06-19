"""Proceduralna tekstura industrijskog terena za budući Mode7 renderer."""

import math

import numpy as np


def generate_terrain_texture(size: int = 512, seed: int = 7) -> np.ndarray:
    """Stvori determinističku RGB teksturu bez vanjskih slikovnih datoteka."""
    if isinstance(size, bool) or not isinstance(size, int) or size < 64:
        raise ValueError("texture size must be an integer of at least 64 pixels")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("texture seed must be a non-negative integer")

    rng = np.random.default_rng(seed)
    phases = rng.uniform(0.0, math.tau, size=4)

    # Kutne koordinate čine sinusne uzorke periodičnima, što ublažava prijelaz pri omatanju.
    coordinates = np.arange(size, dtype=np.float64) * math.tau / size
    angle_x, angle_y = np.meshgrid(coordinates, coordinates)
    field = (
        np.sin(3 * angle_x + phases[0])
        + np.cos(4 * angle_y + phases[1])
        + 0.55 * np.sin(2 * (angle_x + angle_y) + phases[2])
        + 0.35 * np.cos(5 * angle_x - 3 * angle_y + phases[3])
    )
    normalized = (field - field.min()) / np.ptp(field)

    # Osnovna olujno-plava paleta dobiva male kontinuirane varijacije iz polja.
    texture = np.empty((size, size, 3), dtype=np.uint8)
    texture[..., 0] = 34 + normalized * 24
    texture[..., 1] = 48 + normalized * 32
    texture[..., 2] = 58 + normalized * 38

    # Najsvjetliji dijelovi predstavljaju oblake, a najtamniji industrijske zone.
    cloud_mask = normalized > 0.70
    industrial_mask = normalized < 0.25
    texture[cloud_mask] = (91, 108, 117)
    texture[industrial_mask] = (24, 33, 39)

    # Periodična mreža i dijagonala stvaraju mjedene navigacijske linije.
    pixel_y, pixel_x = np.indices((size, size))
    grid_spacing = max(8, size // 8)
    line_width = max(1, size // 256)
    grid_mask = (pixel_x % grid_spacing < line_width) | (
        pixel_y % grid_spacing < line_width
    )
    diagonal_mask = (pixel_x - pixel_y) % size < line_width
    texture[grid_mask | diagonal_mask] = (151, 116, 60)

    return np.ascontiguousarray(texture)
