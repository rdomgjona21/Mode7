import math

import numpy as np
import pytest

from aetherfront.config import HORIZON_Y, INTERNAL_SIZE, WORLD_SIZE
from aetherfront.rendering.camera import Camera
from aetherfront.rendering.mode7 import Mode7Projection


def test_projection_grid_has_expected_shape_and_finite_values() -> None:
    projection = Mode7Projection()

    grid = projection.project(Camera())

    expected_shape = (INTERNAL_SIZE[1] - HORIZON_Y - 1, INTERNAL_SIZE[0])
    assert grid.screen_rows.shape == (expected_shape[0],)
    assert grid.world_x.shape == expected_shape
    assert grid.world_y.shape == expected_shape
    assert np.isfinite(grid.world_x).all()
    assert np.isfinite(grid.world_y).all()


def test_projection_coordinates_stay_inside_wrapped_world() -> None:
    grid = Mode7Projection().project(Camera(x=WORLD_SIZE - 1, y=WORLD_SIZE - 1))

    assert ((0 <= grid.world_x) & (grid.world_x < WORLD_SIZE)).all()
    assert ((0 <= grid.world_y) & (grid.world_y < WORLD_SIZE)).all()


def test_center_column_projects_straight_ahead() -> None:
    projection = Mode7Projection()
    camera = Camera(x=100.0, y=100.0, heading=0.0)

    grid = projection.project(camera)
    center = projection.width // 2

    assert np.all(grid.world_x[:, center] > camera.x)
    assert np.allclose(grid.world_y[:, center], camera.y)


def test_quarter_turn_rotates_forward_direction() -> None:
    projection = Mode7Projection()
    camera = Camera(x=100.0, y=100.0, heading=math.pi / 2)

    grid = projection.project(camera)
    center = projection.width // 2

    assert np.allclose(grid.world_x[:, center], camera.x)
    assert np.all(grid.world_y[:, center] > camera.y)


def test_projection_wraps_forward_samples_at_world_edge() -> None:
    projection = Mode7Projection()
    camera = Camera(x=WORLD_SIZE - 48.0, y=100.0, heading=0.0)

    grid = projection.project(camera)
    center = projection.width // 2

    assert np.any(grid.world_x[:, center] < camera.x)


@pytest.mark.parametrize(
    "overrides, message",
    [
        ({"horizon": -1}, "horizon"),
        ({"horizon": INTERNAL_SIZE[1] - 1}, "horizon"),
        ({"horizontal_fov_degrees": 0}, "FOV"),
        ({"horizontal_fov_degrees": 180}, "FOV"),
        ({"camera_height": 0}, "camera height"),
        ({"max_view_distance": 0}, "view distance"),
        ({"world_size": 0}, "world size"),
    ],
)
def test_projection_rejects_invalid_configuration(
    overrides: dict[str, float | int], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        Mode7Projection(**overrides)
