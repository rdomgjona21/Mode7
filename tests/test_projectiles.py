import math

import pytest

from aetherfront.gameplay.projectiles import Projectile


def _projectile(**overrides: float | str) -> Projectile:
    values: dict[str, float | str] = {
        "x": 100.0,
        "y": 200.0,
        "heading": 0.0,
        "speed": 240.0,
        "damage": 16.0,
        "radius": 4.0,
        "lifetime_remaining": 3.0,
        "team": "player",
        "kind": "cannon",
    }
    values.update(overrides)
    return Projectile(**values)  # type: ignore[arg-type]


def test_projectile_moves_independently_of_frame_division() -> None:
    one_step = _projectile(heading=0.4)
    two_steps = _projectile(heading=0.4)

    one_step.update(1.0)
    two_steps.update(0.5)
    two_steps.update(0.5)

    assert two_steps.x == pytest.approx(one_step.x)
    assert two_steps.y == pytest.approx(one_step.y)
    assert two_steps.lifetime_remaining == pytest.approx(one_step.lifetime_remaining)


def test_projectile_wraps_at_world_boundary() -> None:
    projectile = _projectile(x=2040.0, y=100.0, speed=20.0)

    projectile.update(1.0)

    assert projectile.x == pytest.approx(12.0)
    assert projectile.y == pytest.approx(100.0)


def test_projectile_expires_and_stops_updating() -> None:
    projectile = _projectile(lifetime_remaining=0.5)

    assert not projectile.update(0.5)
    position = (projectile.x, projectile.y)
    assert not projectile.active
    assert not projectile.update(1.0)
    assert (projectile.x, projectile.y) == position


def test_projectile_exposes_collision_body() -> None:
    projectile = _projectile(x=40.0, y=60.0, radius=5.0)

    assert projectile.collision_body.x == 40
    assert projectile.collision_body.y == 60
    assert projectile.collision_body.radius == 5


@pytest.mark.parametrize(
    "overrides, message",
    [
        ({"speed": -1.0}, "speed"),
        ({"damage": -1.0}, "damage"),
        ({"radius": 0.0}, "radius"),
        ({"lifetime_remaining": 0.0}, "lifetime"),
        ({"team": ""}, "team"),
        ({"kind": ""}, "kind"),
        ({"heading": math.inf}, "finite"),
    ],
)
def test_projectile_rejects_invalid_values(
    overrides: dict[str, float | str], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        _projectile(**overrides)
