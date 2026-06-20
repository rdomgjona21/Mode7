import numpy as np
import pygame
import pytest

from aetherfront.config import HORIZON_Y, INTERNAL_SIZE
from aetherfront.rendering.camera import Camera
from aetherfront.rendering.renderer import Mode7Renderer


def test_sampled_ground_has_expected_rgb_shape() -> None:
    ground = Mode7Renderer().sample_ground(Camera())

    assert ground.shape == (INTERNAL_SIZE[1] - HORIZON_Y - 1, INTERNAL_SIZE[0], 3)
    assert ground.dtype == np.uint8
    assert ground.flags.c_contiguous


def test_camera_movement_changes_sampled_ground() -> None:
    renderer = Mode7Renderer()

    first = renderer.sample_ground(Camera(x=100.0, y=100.0, heading=0.0))
    second = renderer.sample_ground(Camera(x=260.0, y=100.0, heading=0.4))

    assert not np.array_equal(first, second)


def test_draw_fills_sky_horizon_and_ground() -> None:
    canvas = pygame.Surface(INTERNAL_SIZE)

    Mode7Renderer().draw(canvas, Camera())
    pixels = pygame.surfarray.array3d(canvas)

    assert np.any(pixels[:, :HORIZON_Y] != 0)
    assert np.all(pixels[:, HORIZON_Y] == (194, 156, 82))
    assert np.unique(pixels[:, HORIZON_Y + 1 :].reshape(-1, 3), axis=0).shape[0] > 8


@pytest.mark.parametrize(
    "texture, message",
    [
        (np.zeros((32, 32), dtype=np.uint8), "RGB shape"),
        (np.zeros((32, 32, 4), dtype=np.uint8), "RGB shape"),
        (np.zeros((32, 32, 3), dtype=np.float64), "uint8"),
    ],
)
def test_renderer_rejects_invalid_texture(texture: np.ndarray, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        Mode7Renderer(texture=texture)


def test_renderer_rejects_incorrect_canvas_size() -> None:
    with pytest.raises(ValueError, match="canvas dimensions"):
        Mode7Renderer().draw(pygame.Surface((320, 180)), Camera())
