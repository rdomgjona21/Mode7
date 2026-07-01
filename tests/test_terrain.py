import csv
import tomllib
from pathlib import Path

import numpy as np
import pytest

from aetherfront.rendering.terrain import (
    AIR_GAP_COLOR,
    BRASS_COLOR,
    BRASS_HIGHLIGHT_COLOR,
    CLOUD_COLOR,
    CLOUD_HIGHLIGHT_COLOR,
    CLOUD_LAYER_PATH,
    CLOUD_SHADOW_COLOR,
    INDUSTRIAL_ISLAND_COLOR,
    INDUSTRIAL_SHADOW_COLOR,
    WOOD_DECK_COLOR,
    generate_terrain_texture,
    load_cloud_texture,
    load_terrain_texture,
)


def test_terrain_texture_has_rgb_shape_and_byte_values() -> None:
    texture = generate_terrain_texture(size=128)

    assert texture.shape == (128, 128, 3)
    assert texture.dtype == np.uint8
    assert texture.flags.c_contiguous
    assert texture.min() >= 0
    assert texture.max() <= 255


def test_cloud_texture_asset_loads_as_contiguous_rgb_array() -> None:
    texture = load_cloud_texture()

    assert texture.ndim == 3
    assert texture.shape[2] == 3
    assert texture.dtype == np.uint8
    assert texture.flags.c_contiguous
    assert texture.min() >= 0
    assert texture.max() <= 255
    assert texture.shape[0] == texture.shape[1]


def test_cloud_texture_asset_is_bright_enough_for_daylight_clouds() -> None:
    texture = load_cloud_texture()

    assert texture.mean() > 150
    assert np.count_nonzero(texture > 220) / texture.size > 0.08


def test_default_terrain_loader_uses_cloud_texture_asset() -> None:
    texture = load_terrain_texture()
    asset_texture = load_cloud_texture()

    assert np.array_equal(texture, asset_texture)


def test_terrain_loader_falls_back_to_procedural_texture_when_asset_is_missing() -> None:
    texture = load_terrain_texture("assets/images/terrain/missing_cloud_layer.png")

    assert texture.shape == (512, 512, 3)
    assert texture.dtype == np.uint8
    assert texture.flags.c_contiguous


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
    assert np.any(np.all(texture == BRASS_COLOR, axis=2))


def test_terrain_texture_contains_airborne_steampunk_elements() -> None:
    texture = generate_terrain_texture(size=160)

    assert np.any(np.all(texture == AIR_GAP_COLOR, axis=2))
    assert np.any(np.all(texture == CLOUD_SHADOW_COLOR, axis=2))
    assert np.any(np.all(texture == CLOUD_COLOR, axis=2))
    assert np.any(np.all(texture == CLOUD_HIGHLIGHT_COLOR, axis=2))
    assert np.any(np.all(texture == INDUSTRIAL_ISLAND_COLOR, axis=2))
    assert np.any(np.all(texture == BRASS_HIGHLIGHT_COLOR, axis=2))


def test_terrain_texture_is_dominated_by_clouds() -> None:
    texture = generate_terrain_texture(size=160)
    cloud_pixels = (
        np.all(texture == CLOUD_SHADOW_COLOR, axis=2)
        | np.all(texture == CLOUD_COLOR, axis=2)
        | np.all(texture == CLOUD_HIGHLIGHT_COLOR, axis=2)
    )
    cloud_ratio = np.count_nonzero(cloud_pixels) / (texture.shape[0] * texture.shape[1])

    assert cloud_ratio > 0.55


def test_terrain_texture_uses_sparse_steampunk_details_instead_of_dense_grid() -> None:
    texture = generate_terrain_texture(size=160)
    brass_pixels = np.all(texture == BRASS_COLOR, axis=2) | np.all(
        texture == BRASS_HIGHLIGHT_COLOR,
        axis=2,
    )
    industrial_pixels = (
        np.all(texture == INDUSTRIAL_ISLAND_COLOR, axis=2)
        | np.all(texture == INDUSTRIAL_SHADOW_COLOR, axis=2)
        | np.all(texture == WOOD_DECK_COLOR, axis=2)
        | brass_pixels
    )
    brass_ratio = np.count_nonzero(brass_pixels) / (texture.shape[0] * texture.shape[1])
    industrial_ratio = np.count_nonzero(industrial_pixels) / (
        texture.shape[0] * texture.shape[1]
    )

    assert 0.002 < brass_ratio < 0.04
    assert industrial_ratio < 0.05


def test_cloud_texture_asset_is_recorded_in_both_manifests() -> None:
    package_manifest = Path("src/aetherfront/assets/manifest.csv")
    docs_manifest = Path("docs/asset-licenses.csv")

    with package_manifest.open(encoding="utf-8", newline="") as handle:
        package_paths = {row["path"] for row in csv.DictReader(handle)}
    with docs_manifest.open(encoding="utf-8", newline="") as handle:
        docs_paths = {row["path"] for row in csv.DictReader(handle)}

    assert CLOUD_LAYER_PATH in package_paths
    assert f"src/aetherfront/{CLOUD_LAYER_PATH}" in docs_paths


def test_package_data_includes_terrain_png_assets() -> None:
    with Path("pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    package_data = pyproject["tool"]["setuptools"]["package-data"]["aetherfront"]

    assert "assets/images/**/*.png" in package_data


@pytest.mark.parametrize("size", [0, 63, 64.5, True])
def test_terrain_texture_rejects_invalid_size(size: object) -> None:
    with pytest.raises(ValueError, match="texture size"):
        generate_terrain_texture(size=size)  # type: ignore[arg-type]


@pytest.mark.parametrize("seed", [-1, 1.5, True])
def test_terrain_texture_rejects_invalid_seed(seed: object) -> None:
    with pytest.raises(ValueError, match="texture seed"):
        generate_terrain_texture(seed=seed)  # type: ignore[arg-type]
