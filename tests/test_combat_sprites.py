import pygame

from aetherfront.gameplay.enemies import EnemyKind
from aetherfront.rendering.combat_sprites import (
    create_boss_surface,
    create_enemy_surfaces,
    create_projectile_surfaces,
    create_repair_surface,
)


def test_enemy_surfaces_cover_all_standard_enemy_kinds() -> None:
    surfaces = create_enemy_surfaces()

    assert set(surfaces) == {EnemyKind.SCOUT, EnemyKind.GUNSHIP, EnemyKind.BOMBER}
    assert surfaces[EnemyKind.SCOUT].get_size()[0] < surfaces[EnemyKind.BOMBER].get_size()[0]
    assert any(surfaces[EnemyKind.GUNSHIP].get_at((x, 22)).a for x in range(56))


def test_enemy_surfaces_use_distinct_victorian_airship_sizes() -> None:
    surfaces = create_enemy_surfaces()

    assert surfaces[EnemyKind.SCOUT].get_size() == (42, 28)
    assert surfaces[EnemyKind.GUNSHIP].get_size() == (56, 34)
    assert surfaces[EnemyKind.BOMBER].get_size() == (70, 44)


def test_projectile_surfaces_include_enemy_projectiles() -> None:
    surfaces = create_projectile_surfaces()

    assert {"cannon", "spread", "rocket", "enemy_light", "enemy_heavy"} <= set(surfaces)
    assert isinstance(surfaces["enemy_heavy"], pygame.Surface)


def test_boss_surface_is_larger_than_standard_enemies() -> None:
    boss = create_boss_surface()
    enemies = create_enemy_surfaces()

    assert boss.get_width() > enemies[EnemyKind.BOMBER].get_width()
    assert boss.get_height() > enemies[EnemyKind.BOMBER].get_height()
    assert any(boss.get_at((x, 39)).a for x in range(boss.get_width()))


def test_boss_surface_contains_several_visible_detail_colors() -> None:
    boss = create_boss_surface()
    visible_colors = {
        boss.get_at((x, y))[:3]
        for x in range(boss.get_width())
        for y in range(boss.get_height())
        if boss.get_at((x, y)).a
    }

    assert len(visible_colors) >= 8


def test_repair_surface_remains_visible_and_transparent() -> None:
    surface = create_repair_surface()
    alpha_values = [
        surface.get_at((x, y)).a
        for x in range(surface.get_width())
        for y in range(surface.get_height())
    ]

    assert surface.get_size() == (32, 32)
    assert min(alpha_values) == 0
    assert max(alpha_values) > 0
