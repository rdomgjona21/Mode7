import numpy as np
import pytest

from aetherfront.rendering.terrain import generate_terrain_texture


def test_terrain_texture_has_rgb_shape_and_byte_values() -> None:
    texture = generate_terrain_texture(size=128)

    assert texture.shape == (128, 128, 3)
    assert texture.dtype == np.uint8
    assert texture.flags.c_contiguous
    assert texture.min() >= 0
    assert texture.max() <= 255


def test_terrain_texture_is_deterministic_for_same_seed() -> None:
    first = generate_terrain_texture(size=96, seed=21)
    second = generate_terrain_texture(size=96, seed=21)

    assert np.array_equal(first, second)


def test_terrain_texture_changes_with_seed() -> None:
    first = generate_terrain_texture(size=96, seed=1)
    second = generate_terrain_texture(size=96, seed=2)

    assert not np.array_equal(first, second)


def test_terrain_texture_contains_visual_variation() -> None:
    texture = generate_terrain_texture(size=128)
    unique_colors = np.unique(texture.reshape(-1, 3), axis=0)

    assert len(unique_colors) > 32
    assert np.any(np.all(texture == (151, 116, 60), axis=2))


@pytest.mark.parametrize("size", [0, 63, 64.5, True])
def test_terrain_texture_rejects_invalid_size(size: object) -> None:
    with pytest.raises(ValueError, match="texture size"):
        generate_terrain_texture(size=size)  # type: ignore[arg-type]


@pytest.mark.parametrize("seed", [-1, 1.5, True])
def test_terrain_texture_rejects_invalid_seed(seed: object) -> None:
    with pytest.raises(ValueError, match="texture seed"):
        generate_terrain_texture(seed=seed)  # type: ignore[arg-type]
