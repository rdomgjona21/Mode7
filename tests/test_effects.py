import numpy as np
import pygame

from aetherfront.config import INTERNAL_SIZE
from aetherfront.rendering.billboards import BillboardProjector, WorldBillboard
from aetherfront.rendering.camera import Camera
from aetherfront.rendering.effects import (
    EXPLOSION_LIFETIME,
    MUZZLE_FLASH_LIFETIME,
    PLAYER_HIT_LIFETIME,
    EffectKind,
    EffectsState,
    WorldEffect,
    create_world_effect_surface,
    draw_muzzle_flash,
    draw_player_hit_marker,
)


def test_explosion_effect_expires_after_lifetime() -> None:
    effects = EffectsState()
    effects.add_explosion(100, 200)

    effects.update(EXPLOSION_LIFETIME + 0.01)

    assert effects.world_effects == []


def test_effects_do_not_update_while_paused() -> None:
    effects = EffectsState()
    effects.add_explosion(100, 200)
    effects.trigger_muzzle_flash()
    effects.trigger_player_hit()

    effects.update(10.0, paused=True)

    assert len(effects.world_effects) == 1
    assert effects.muzzle_flash_remaining == MUZZLE_FLASH_LIFETIME
    assert effects.player_hit_remaining == PLAYER_HIT_LIFETIME


def test_world_effect_projection_uses_camera_heading() -> None:
    projector = BillboardProjector()
    surface = create_world_effect_surface(
        WorldEffect(EffectKind.EXPLOSION, 300, 100, 1, 1, 40)
    )
    billboard = WorldBillboard(surface, 300, 100, 40)

    straight = projector.project(Camera(x=100, y=100, heading=0), billboard)
    turned = projector.project(Camera(x=100, y=100, heading=0.4), billboard)

    assert straight is not None
    assert turned is not None
    assert straight.rect.centerx != turned.rect.centerx


def test_player_hit_marker_draws_visible_pixels_headless() -> None:
    canvas = pygame.Surface(INTERNAL_SIZE)

    draw_player_hit_marker(canvas, intensity=1.0)

    assert np.any(pygame.surfarray.array3d(canvas) != 0)


def test_muzzle_flash_draws_visible_pixels_headless() -> None:
    canvas = pygame.Surface(INTERNAL_SIZE)

    draw_muzzle_flash(canvas, intensity=1.0)

    assert np.any(pygame.surfarray.array3d(canvas) != 0)


def test_effects_draw_world_and_local_feedback_headless() -> None:
    canvas = pygame.Surface(INTERNAL_SIZE)
    camera = Camera(x=100, y=100, heading=0)
    effects = EffectsState()
    effects.add_explosion(320, 100)
    effects.trigger_muzzle_flash()
    effects.trigger_player_hit()

    effects.draw(canvas, camera, BillboardProjector())

    assert np.any(pygame.surfarray.array3d(canvas) != 0)
