"""Proceduralna tekstura oblačnog sloja za Mode7 renderer."""

import math
from importlib.resources import as_file, files

import numpy as np
import pygame

TERRAIN_ASSET_PACKAGE = "aetherfront"
CLOUD_LAYER_PATH = "assets/images/terrain/cloud_layer.png"
AIR_GAP_COLOR = (17, 28, 43)
CLOUD_SHADOW_COLOR = (58, 76, 89)
CLOUD_COLOR = (91, 108, 117)
CLOUD_HIGHLIGHT_COLOR = (122, 139, 145)
INDUSTRIAL_ISLAND_COLOR = (27, 35, 39)
INDUSTRIAL_SHADOW_COLOR = (18, 25, 30)
BRASS_COLOR = (166, 125, 58)
BRASS_HIGHLIGHT_COLOR = (210, 164, 78)
WOOD_DECK_COLOR = (89, 61, 39)


def load_cloud_texture(path: str = CLOUD_LAYER_PATH) -> np.ndarray:
    """Učitaj projektni PNG oblačni sloj kao RGB NumPy teksturu."""
    resource = files(TERRAIN_ASSET_PACKAGE).joinpath(*path.split("/"))
    if not resource.is_file():
        raise FileNotFoundError(path)

    with as_file(resource) as asset_path:
        surface = pygame.image.load(str(asset_path))

    pixels = pygame.surfarray.array3d(surface)
    return np.ascontiguousarray(np.swapaxes(pixels[:, :, :3], 0, 1), dtype=np.uint8)


def load_terrain_texture(path: str = CLOUD_LAYER_PATH) -> np.ndarray:
    """Učitaj cloud asset, a proceduralni generator koristi samo ako asset nije dostupan."""
    try:
        return load_cloud_texture(path)
    except (FileNotFoundError, OSError, pygame.error):
        return generate_terrain_texture()


def generate_terrain_texture(size: int = 512, seed: int = 7) -> np.ndarray:
    """Stvori determinističku RGB teksturu gustih oblaka bez vanjskih asseta."""
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

    # Osnovna paleta sada je oblačna, a ne zemljana. Kontinuirana varijacija sprječava
    # da veliki oblačni slojevi izgledaju kao ravna jednobojna ploha.
    texture = np.empty((size, size, 3), dtype=np.uint8)
    texture[..., 0] = 58 + normalized * 40
    texture[..., 1] = 75 + normalized * 42
    texture[..., 2] = 88 + normalized * 40

    cloud_field = (
        normalized
        + 0.18 * np.sin(7 * angle_x - 2 * angle_y + phases[0])
        + 0.10 * np.cos(9 * angle_x + 5 * angle_y + phases[1])
    )
    air_gap_mask = cloud_field < 0.20
    cloud_shadow_mask = (cloud_field >= 0.20) & (cloud_field < 0.40)
    cloud_mask = cloud_field > 0.56
    cloud_highlight_mask = cloud_field > 0.72
    texture[air_gap_mask] = AIR_GAP_COLOR
    texture[cloud_shadow_mask] = CLOUD_SHADOW_COLOR
    texture[cloud_mask] = CLOUD_COLOR
    texture[cloud_highlight_mask] = CLOUD_HIGHLIGHT_COLOR

    # Steampunk elementi ostaju samo rijetki orijentiri u oblačnom moru. Ne smiju
    # dominirati podlogom jer bi igra opet djelovala kao da se kreće po čvrstom tlu.
    pixel_y, pixel_x = np.indices((size, size))
    cell_size = max(80, size // 3)
    cell_x = pixel_x // cell_size
    cell_y = pixel_y // cell_size
    local_x = (pixel_x % cell_size) / cell_size - 0.5
    local_y = (pixel_y % cell_size) / cell_size - 0.5
    cell_selector = (cell_x * 17 + cell_y * 29 + seed * 11) % 9
    active_cell = cell_selector == 4
    ellipse_value = (local_x / 0.30) ** 2 + (local_y / 0.13) ** 2
    island_mask = active_cell & (ellipse_value < 1.0)
    island_shadow_mask = island_mask & (local_y > 0.055)
    island_rim_mask = active_cell & (ellipse_value > 0.76) & (ellipse_value < 1.02)

    texture[island_mask] = INDUSTRIAL_ISLAND_COLOR
    texture[island_shadow_mask] = INDUSTRIAL_SHADOW_COLOR
    texture[island_rim_mask] = BRASS_COLOR

    runway_mask = island_mask & (np.abs(local_y) < 0.018)
    deck_mask = island_mask & (np.abs(local_x) < 0.038) & (np.abs(local_y) < 0.11)
    texture[runway_mask] = BRASS_COLOR
    texture[deck_mask] = WOOD_DECK_COLOR

    turbine_left = ((local_x + 0.16) ** 2 + (local_y + 0.01) ** 2) ** 0.5
    turbine_right = ((local_x - 0.16) ** 2 + (local_y - 0.01) ** 2) ** 0.5
    turbine_ring_mask = active_cell & (
        ((turbine_left > 0.042) & (turbine_left < 0.057))
        | ((turbine_right > 0.042) & (turbine_right < 0.057))
    )
    turbine_core_mask = active_cell & ((turbine_left < 0.017) | (turbine_right < 0.017))
    texture[turbine_ring_mask] = BRASS_HIGHLIGHT_COLOR
    texture[turbine_core_mask] = CLOUD_HIGHLIGHT_COLOR

    bridge_selector = (cell_x * 5 + cell_y * 3 + seed) % 11
    bridge_mask = (
        (bridge_selector == 0)
        & (np.abs(local_x + local_y) < 0.010)
        & (np.abs(local_x) < 0.32)
        & (np.abs(local_y) < 0.24)
    )
    texture[bridge_mask] = BRASS_COLOR

    return np.ascontiguousarray(texture)
