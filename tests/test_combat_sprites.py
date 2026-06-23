import pygame

from aetherfront.gameplay.enemies import EnemyKind
from aetherfront.rendering.combat_sprites import (
    create_boss_surface,
    create_enemy_surfaces,
    create_projectile_surfaces,
)


def test_enemy_surfaces_cover_all_standard_enemy_kinds() -> None:
    surfaces = create_enemy_surfaces()

    assert set(surfaces) == {EnemyKind.SCOUT, EnemyKind.GUNSHIP, EnemyKind.BOMBER}
    assert surfaces[EnemyKind.SCOUT].get_size()[0] < surfaces[EnemyKind.BOMBER].get_size()[0]
    assert any(surfaces[EnemyKind.GUNSHIP].get_at((x, 22)).a for x in range(56))


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
