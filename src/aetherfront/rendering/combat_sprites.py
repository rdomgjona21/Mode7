"""Proceduralne slike projektila, protivnika i popravka."""

import pygame

from aetherfront.gameplay.enemies import EnemyKind


def create_projectile_surfaces() -> dict[str, pygame.Surface]:
    """Stvori prepoznatljive slike za igračeve i neprijateljske projektile."""
    cannon = pygame.Surface((12, 6), pygame.SRCALPHA)
    pygame.draw.ellipse(cannon, (236, 190, 83), cannon.get_rect())
    pygame.draw.circle(cannon, (255, 239, 168), (9, 3), 2)

    spread = pygame.Surface((10, 6), pygame.SRCALPHA)
    pygame.draw.polygon(spread, (62, 220, 225), ((0, 3), (7, 0), (10, 3), (7, 6)))

    rocket = pygame.Surface((18, 9), pygame.SRCALPHA)
    pygame.draw.polygon(rocket, (197, 76, 54), ((0, 1), (12, 1), (18, 4), (12, 8), (0, 8)))
    pygame.draw.polygon(rocket, (242, 187, 67), ((0, 2), (0, 7), (5, 4)))

    enemy_light = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.circle(enemy_light, (210, 77, 60), (5, 5), 4)
    pygame.draw.circle(enemy_light, (255, 171, 91), (5, 5), 2)

    enemy_heavy = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.circle(enemy_heavy, (113, 43, 47), (8, 8), 7)
    pygame.draw.circle(enemy_heavy, (237, 96, 74), (8, 8), 5)
    pygame.draw.circle(enemy_heavy, (255, 202, 104), (8, 8), 2)
    return {
        "cannon": cannon,
        "spread": spread,
        "rocket": rocket,
        "enemy_light": enemy_light,
        "enemy_heavy": enemy_heavy,
    }


def create_enemy_surfaces() -> dict[EnemyKind, pygame.Surface]:
    """Stvori tri proceduralna zračna broda bez vanjskih asseta."""
    scout = pygame.Surface((42, 28), pygame.SRCALPHA)
    pygame.draw.ellipse(scout, (93, 70, 52), (5, 4, 30, 12))
    pygame.draw.polygon(scout, (209, 154, 68), ((5, 17), (31, 17), (38, 22), (11, 24)))
    pygame.draw.polygon(scout, (62, 211, 202), ((32, 8), (41, 14), (32, 20)))
    pygame.draw.line(scout, (232, 220, 181), (12, 17), (30, 17), 2)

    gunship = pygame.Surface((56, 34), pygame.SRCALPHA)
    pygame.draw.ellipse(gunship, (74, 57, 50), (5, 3, 42, 15))
    pygame.draw.rect(gunship, (157, 111, 59), (10, 18, 34, 8))
    pygame.draw.polygon(gunship, (46, 52, 61), ((44, 19), (55, 23), (44, 27)))
    pygame.draw.line(gunship, (221, 190, 108), (14, 22), (41, 22), 3)
    pygame.draw.circle(gunship, (65, 211, 202), (42, 22), 3)

    bomber = pygame.Surface((70, 44), pygame.SRCALPHA)
    pygame.draw.ellipse(bomber, (64, 54, 48), (8, 3, 50, 18))
    pygame.draw.rect(bomber, (112, 78, 57), (12, 22, 43, 12))
    pygame.draw.polygon(bomber, (42, 45, 52), ((54, 22), (69, 29), (54, 36)))
    pygame.draw.circle(bomber, (189, 71, 57), (22, 28), 5)
    pygame.draw.circle(bomber, (189, 71, 57), (42, 28), 5)
    pygame.draw.line(bomber, (222, 205, 158), (15, 22), (51, 22), 3)
    return {
        EnemyKind.SCOUT: scout,
        EnemyKind.GUNSHIP: gunship,
        EnemyKind.BOMBER: bomber,
    }


def create_repair_surface() -> pygame.Surface:
    """Stvori cijan ćeliju s križem koja označava popravak."""
    surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(surface, (34, 73, 78), (16, 16), 14)
    pygame.draw.circle(surface, (65, 211, 202), (16, 16), 12, 3)
    pygame.draw.rect(surface, (231, 222, 179), (13, 7, 6, 18))
    pygame.draw.rect(surface, (231, 222, 179), (7, 13, 18, 6))
    return surface
