import pytest

from aetherfront.config import WORLD_SIZE
from aetherfront.gameplay.collisions import CircleBody, circles_overlap, wrapped_axis_delta


def test_overlapping_circles_collide() -> None:
    assert circles_overlap(CircleBody(100, 100, 10), CircleBody(115, 100, 6))


def test_separated_circles_do_not_collide() -> None:
    assert not circles_overlap(CircleBody(100, 100, 10), CircleBody(121, 100, 10))


def test_touching_circles_count_as_collision() -> None:
    assert circles_overlap(CircleBody(100, 100, 10), CircleBody(120, 100, 10))


def test_collision_uses_shortest_distance_across_world_boundary() -> None:
    first = CircleBody(WORLD_SIZE - 5, 200, 8)
    second = CircleBody(4, 200, 4)

    assert circles_overlap(first, second)
    assert wrapped_axis_delta(first.x, second.x) == pytest.approx(9)


def test_circle_rejects_invalid_radius() -> None:
    with pytest.raises(ValueError, match="radius"):
        CircleBody(100, 100, 0)
