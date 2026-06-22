import math

import pygame
import pytest

from aetherfront.config import INTERNAL_SIZE, WORLD_SIZE
from aetherfront.rendering.billboards import BillboardProjector, WorldBillboard
from aetherfront.rendering.camera import Camera


def _billboard(x: float, y: float, width: float = 24.0) -> WorldBillboard:
    return WorldBillboard(pygame.Surface((24, 12), pygame.SRCALPHA), x, y, width)


def test_projection_uses_shortest_distance_across_world_boundary() -> None:
    camera = Camera(x=WORLD_SIZE - 100, y=200.0, heading=0.0)

    projected = BillboardProjector().project(camera, _billboard(100.0, 200.0))

    assert projected is not None
    assert projected.depth == pytest.approx(200.0)


def test_billboard_behind_camera_is_culled() -> None:
    camera = Camera(x=300.0, y=300.0, heading=0.0)

    assert BillboardProjector().project(camera, _billboard(250.0, 300.0)) is None


def test_nearer_billboard_is_projected_larger() -> None:
    projector = BillboardProjector()
    camera = Camera(x=100.0, y=100.0, heading=0.0)

    near = projector.project(camera, _billboard(280.0, 100.0))
    far = projector.project(camera, _billboard(420.0, 100.0))

    assert near is not None and far is not None
    assert near.rect.width > far.rect.width
    assert near.rect.height > far.rect.height


def test_camera_rotation_changes_horizontal_projection() -> None:
    projector = BillboardProjector()
    billboard = _billboard(300.0, 140.0)

    straight = projector.project(Camera(x=100.0, y=100.0, heading=0.0), billboard)
    turned = projector.project(Camera(x=100.0, y=100.0, heading=math.pi / 8), billboard)

    assert straight is not None and turned is not None
    assert straight.rect.centerx != turned.rect.centerx


def test_project_all_sorts_far_to_near_and_omits_hidden_objects() -> None:
    projector = BillboardProjector()
    camera = Camera(x=100.0, y=100.0, heading=0.0)
    objects = (
        _billboard(280.0, 100.0),
        _billboard(420.0, 100.0),
        _billboard(50.0, 100.0),
    )

    projected = projector.project_all(camera, objects)

    assert [item.depth for item in projected] == pytest.approx([320.0, 180.0])


def test_draw_rejects_wrong_canvas_size() -> None:
    with pytest.raises(ValueError, match="canvas dimensions"):
        BillboardProjector().draw(pygame.Surface((320, 180)), Camera(), ())


def test_draw_returns_number_of_visible_objects() -> None:
    canvas = pygame.Surface(INTERNAL_SIZE, pygame.SRCALPHA)
    camera = Camera(x=100.0, y=100.0, heading=0.0)

    drawn = BillboardProjector().draw(canvas, camera, (_billboard(300.0, 100.0),))

    assert drawn == 1
