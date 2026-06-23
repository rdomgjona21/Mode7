import numpy as np
import pygame
import pytest

from aetherfront.config import HORIZON_Y, INTERNAL_SIZE
from aetherfront.rendering.parallax import (
    PARALLAX_SKY_SIZE,
    ParallaxSkyLayer,
    create_parallax_sky_layers,
)


def test_parallax_sky_size_matches_horizon_area() -> None:
    assert PARALLAX_SKY_SIZE == (INTERNAL_SIZE[0], HORIZON_Y + 1)


def test_create_parallax_layers_returns_three_named_layers() -> None:
    layers = create_parallax_sky_layers()

    assert [layer.name for layer in layers] == [
        "far_clouds",
        "industrial_haze",
        "near_streaks",
    ]


def test_parallax_layers_have_valid_size_and_visible_pixels() -> None:
    for layer in create_parallax_sky_layers():
        assert layer.surface.get_size() == PARALLAX_SKY_SIZE
        assert np.any(pygame.surfarray.array_alpha(layer.surface) != 0)


def test_parallax_layers_are_deterministic_for_same_seed() -> None:
    first = create_parallax_sky_layers(seed=5)
    second = create_parallax_sky_layers(seed=5)

    for first_layer, second_layer in zip(first, second, strict=True):
        assert np.array_equal(
            pygame.surfarray.array3d(first_layer.surface),
            pygame.surfarray.array3d(second_layer.surface),
        )
        assert np.array_equal(
            pygame.surfarray.array_alpha(first_layer.surface),
            pygame.surfarray.array_alpha(second_layer.surface),
        )


def test_parallax_layers_change_with_different_seed() -> None:
    first = create_parallax_sky_layers(seed=5)
    second = create_parallax_sky_layers(seed=6)

    assert any(
        not np.array_equal(
            pygame.surfarray.array_alpha(first_layer.surface),
            pygame.surfarray.array_alpha(second_layer.surface),
        )
        for first_layer, second_layer in zip(first, second, strict=True)
    )


def test_parallax_layers_use_distinct_scroll_factors() -> None:
    scroll_factors = [layer.scroll_factor for layer in create_parallax_sky_layers()]

    assert scroll_factors == sorted(scroll_factors)
    assert len(set(scroll_factors)) == 3


def test_parallax_layer_rejects_wrong_surface_size() -> None:
    with pytest.raises(ValueError, match="size"):
        ParallaxSkyLayer("bad", pygame.Surface((10, 10), pygame.SRCALPHA), 0.1, 100)


@pytest.mark.parametrize("seed", [1.5, True, "17"])
def test_create_parallax_layers_rejects_invalid_seed(seed: object) -> None:
    with pytest.raises(ValueError, match="seed"):
        create_parallax_sky_layers(seed=seed)  # type: ignore[arg-type]
