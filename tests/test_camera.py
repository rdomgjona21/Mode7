import math

import pytest

from aetherfront.config import MAX_SPEED, MIN_SPEED, TURN_RATE, WORLD_SIZE
from aetherfront.rendering.camera import Camera


def test_camera_moves_forward_for_elapsed_time() -> None:
    camera = Camera(x=100.0, y=200.0, heading=0.0, speed=50.0)

    camera.update(dt=2.0)

    assert camera.x == pytest.approx(200.0)
    assert camera.y == pytest.approx(200.0)


def test_camera_movement_is_independent_of_frame_division() -> None:
    one_step = Camera(x=100.0, y=200.0, heading=0.5, speed=50.0)
    two_steps = Camera(x=100.0, y=200.0, heading=0.5, speed=50.0)

    one_step.update(dt=1.0)
    two_steps.update(dt=0.5)
    two_steps.update(dt=0.5)

    assert two_steps.x == pytest.approx(one_step.x)
    assert two_steps.y == pytest.approx(one_step.y)


def test_camera_speed_stays_within_limits() -> None:
    camera = Camera(speed=MIN_SPEED)
    camera.update(dt=0.5, throttle=1.0)
    assert camera.speed == pytest.approx(38.0)

    camera.speed = MAX_SPEED
    camera.update(dt=10.0, throttle=1.0)
    assert camera.speed == MAX_SPEED

    camera.speed = MIN_SPEED
    camera.update(dt=10.0, throttle=-1.0)
    assert camera.speed == MIN_SPEED


def test_camera_heading_wraps_after_full_rotation() -> None:
    camera = Camera(heading=0.0)

    camera.update(dt=math.tau / TURN_RATE, turn=1.0)

    assert camera.heading == pytest.approx(0.0, abs=1e-12)


def test_camera_position_wraps_at_world_edge() -> None:
    camera = Camera(x=WORLD_SIZE - 8.0, y=100.0, heading=0.0, speed=20.0)

    camera.update(dt=1.0)

    assert camera.x == pytest.approx(12.0)
    assert camera.y == pytest.approx(100.0)


def test_camera_rejects_negative_delta_time() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        Camera().update(dt=-0.01)
