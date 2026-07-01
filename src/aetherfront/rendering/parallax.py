"""Proceduralni parallax slojevi neba pripremljeni za kasnije renderiranje."""

from dataclasses import dataclass

import numpy as np
import pygame

from aetherfront.config import HORIZON_Y, INTERNAL_SIZE

PARALLAX_SKY_SIZE = (INTERNAL_SIZE[0], HORIZON_Y + 1)


@dataclass(frozen=True, slots=True)
class ParallaxSkyLayer:
    """Jedan proceduralni sloj neba s budućim faktorom sporijeg pomaka."""

    name: str
    surface: pygame.Surface
    scroll_factor: float
    opacity: int

    def __post_init__(self) -> None:
        if self.surface.get_size() != PARALLAX_SKY_SIZE:
            raise ValueError("parallax layer size must match the sky area")
        if not 0.0 <= self.scroll_factor <= 1.0:
            raise ValueError("parallax scroll factor must be between 0 and 1")
        if not 0 <= self.opacity <= 255:
            raise ValueError("parallax opacity must be between 0 and 255")


def create_parallax_sky_layers(seed: int = 17) -> tuple[ParallaxSkyLayer, ...]:
    """Stvori tri deterministička RGBA sloja za budući parallax neba."""
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("parallax seed must be an integer")

    width, height = PARALLAX_SKY_SIZE
    far_clouds = _surface_from_array(
        _far_cloud_pixels(width, height, seed),
    )
    industrial_haze = _surface_from_array(
        _industrial_haze_pixels(width, height, seed + 11),
    )
    near_streaks = _surface_from_array(
        _near_streak_pixels(width, height, seed + 23),
    )
    return (
        ParallaxSkyLayer("far_clouds", far_clouds, scroll_factor=0.05, opacity=52),
        ParallaxSkyLayer("industrial_haze", industrial_haze, scroll_factor=0.11, opacity=64),
        ParallaxSkyLayer("near_streaks", near_streaks, scroll_factor=0.18, opacity=78),
    )


def _surface_from_array(pixels: np.ndarray) -> pygame.Surface:
    """Pretvori RGBA matricu oblika height×width×4 u PyGame površinu."""
    surface = pygame.Surface(PARALLAX_SKY_SIZE, pygame.SRCALPHA)
    pygame.surfarray.blit_array(surface, np.swapaxes(pixels[:, :, :3], 0, 1))
    pygame.surfarray.pixels_alpha(surface)[:, :] = np.swapaxes(pixels[:, :, 3], 0, 1)
    return surface


def _far_cloud_pixels(width: int, height: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    y = np.linspace(0.0, 1.0, height, dtype=np.float64)[:, np.newaxis]
    x = np.linspace(0.0, 1.0, width, dtype=np.float64)[np.newaxis, :]
    wave = np.sin((x * 5.5 + seed * 0.01) * np.pi) + np.cos((x * 2.0 + y * 2.5) * np.pi)
    noise = rng.normal(0.0, 0.10, size=(height, width))
    mask = wave + noise > 0.58
    pixels = np.zeros((height, width, 4), dtype=np.uint8)
    pixels[mask] = (122, 142, 151, 42)
    for _ in range(5):
        center_x = int(rng.integers(20, width - 20))
        center_y = int(rng.integers(10, max(11, round(height * 0.55))))
        radius_x = int(rng.integers(5, 10))
        radius_y = int(rng.integers(7, 13))
        yy, xx = np.ogrid[:height, :width]
        balloon = ((xx - center_x) / radius_x) ** 2 + ((yy - center_y) / radius_y) ** 2 <= 1.0
        gondola_top = min(height, center_y + radius_y + 2)
        gondola_bottom = min(height, gondola_top + 2)
        pixels[balloon] = (118, 134, 139, 44)
        pixels[gondola_top:gondola_bottom, center_x - 3 : center_x + 4] = (165, 119, 56, 42)
    return pixels


def _industrial_haze_pixels(width: int, height: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pixels = np.zeros((height, width, 4), dtype=np.uint8)
    skyline_y = round(height * 0.72)
    for cluster_x in range(-20, width, 74):
        island_width = int(rng.integers(38, 68))
        island_y = int(skyline_y + rng.integers(-9, 8))
        left = max(0, cluster_x + int(rng.integers(-8, 9)))
        right = min(width, left + island_width)
        if right <= left:
            continue

        pixels[island_y : min(height, island_y + 3), left:right] = (167, 124, 58, 60)
        pixels[min(height - 1, island_y + 3) : min(height, island_y + 8), left + 4 : right - 4] = (
            20,
            31,
            38,
            58,
        )
        for column in range(left + 6, max(left + 7, right - 8), 9):
            building_width = int(rng.integers(5, 11))
            building_height = int(rng.integers(12, 36))
            top = max(7, island_y - building_height)
            building_right = min(right, column + building_width)
            pixels[top:island_y, column:building_right] = (24, 35, 42, 58)
            if rng.random() > 0.50:
                pixels[top : min(island_y, top + 2), column:building_right] = (
                    173,
                    130,
                    62,
                    62,
                )
            if rng.random() > 0.62:
                stack_x = min(width - 2, column + building_width // 2)
                stack_top = max(5, top - int(rng.integers(4, 12)))
                pixels[stack_top:top, stack_x : stack_x + 2] = (33, 31, 29, 58)
                for puff in range(3):
                    puff_y = max(2, stack_top - 4 - puff * 5)
                    puff_x = max(0, min(width - 7, stack_x - 2 + puff * 2))
                    pixels[puff_y : puff_y + 4, puff_x : puff_x + 7] = (106, 122, 121, 34)
    return pixels


def _near_streak_pixels(width: int, height: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pixels = np.zeros((height, width, 4), dtype=np.uint8)
    for _ in range(34):
        y = int(rng.integers(round(height * 0.35), height - 4))
        x = int(rng.integers(0, width))
        length = int(rng.integers(18, 72))
        thickness = int(rng.integers(1, 3))
        color = (183, 153, 91, int(rng.integers(38, 76)))
        end = min(width, x + length)
        pixels[y : y + thickness, x:end] = color
    return pixels
