"""Proceduralne slike projektila, protivnika i popravka."""

import pygame

from aetherfront.gameplay.enemies import EnemyKind

BRASS = (204, 158, 72)
BRIGHT_BRASS = (235, 202, 120)
DARK_WOOD = (73, 50, 37)
WARM_WOOD = (143, 95, 51)
CANVAS = (117, 129, 121)
CANVAS_LIGHT = (168, 177, 157)
IRON = (40, 44, 50)
AETHER = (62, 211, 202)


def _rivet_row(surface: pygame.Surface, y: int, xs: tuple[int, ...]) -> None:
    for x in xs:
        pygame.draw.circle(surface, BRIGHT_BRASS, (x, y), 1)


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
    """Stvori tri viktorijanska proceduralna zračna broda bez vanjskih asseta."""
    scout = pygame.Surface((42, 28), pygame.SRCALPHA)
    pygame.draw.ellipse(scout, (80, 70, 58), (4, 2, 31, 12))
    pygame.draw.ellipse(scout, (144, 127, 94), (8, 4, 24, 7))
    pygame.draw.line(scout, BRASS, (12, 14), (15, 18), 1)
    pygame.draw.line(scout, BRASS, (28, 14), (25, 18), 1)
    pygame.draw.polygon(scout, DARK_WOOD, ((7, 17), (31, 17), (38, 22), (12, 25)))
    pygame.draw.polygon(scout, BRASS, ((8, 18), (29, 18), (34, 22), (13, 23)))
    pygame.draw.polygon(scout, AETHER, ((31, 8), (41, 14), (31, 20)))
    pygame.draw.circle(scout, BRIGHT_BRASS, (20, 20), 2)
    _rivet_row(scout, 18, (12, 18, 24, 30))

    gunship = pygame.Surface((56, 34), pygame.SRCALPHA)
    pygame.draw.ellipse(gunship, (55, 58, 58), (5, 2, 43, 16))
    pygame.draw.ellipse(gunship, CANVAS, (9, 4, 36, 11))
    for x in (17, 29, 41):
        pygame.draw.arc(gunship, (71, 83, 82), (x - 6, 4, 12, 12), 1.4, 4.9, 1)
    pygame.draw.line(gunship, BRASS, (13, 17), (17, 22), 2)
    pygame.draw.line(gunship, BRASS, (41, 17), (36, 22), 2)
    pygame.draw.rect(gunship, WARM_WOOD, (10, 20, 34, 8), border_radius=2)
    pygame.draw.rect(gunship, DARK_WOOD, (9, 25, 36, 4), border_radius=2)
    pygame.draw.polygon(gunship, IRON, ((44, 20), (55, 24), (44, 28)))
    pygame.draw.line(gunship, BRIGHT_BRASS, (13, 22), (41, 22), 2)
    pygame.draw.circle(gunship, AETHER, (40, 24), 3)
    _rivet_row(gunship, 26, (15, 22, 29, 36))

    bomber = pygame.Surface((70, 44), pygame.SRCALPHA)
    pygame.draw.ellipse(bomber, (49, 47, 43), (6, 2, 54, 20))
    pygame.draw.ellipse(bomber, (104, 91, 70), (11, 5, 45, 13))
    for x in (18, 31, 44, 55):
        pygame.draw.arc(bomber, (72, 72, 64), (x - 7, 5, 14, 16), 1.35, 4.95, 1)
    pygame.draw.line(bomber, BRASS, (17, 21), (22, 28), 2)
    pygame.draw.line(bomber, BRASS, (50, 21), (45, 28), 2)
    pygame.draw.rect(bomber, (103, 68, 47), (12, 26, 43, 11), border_radius=2)
    pygame.draw.rect(bomber, DARK_WOOD, (14, 34, 40, 5), border_radius=2)
    pygame.draw.polygon(bomber, IRON, ((54, 25), (69, 31), (54, 38)))
    pygame.draw.circle(bomber, (193, 63, 57), (23, 31), 5)
    pygame.draw.circle(bomber, (193, 63, 57), (43, 31), 5)
    pygame.draw.line(bomber, BRIGHT_BRASS, (16, 26), (52, 26), 2)
    _rivet_row(bomber, 36, (18, 25, 32, 39, 46))
    pygame.draw.rect(bomber, IRON, (31, 20, 5, 9))
    pygame.draw.rect(bomber, BRASS, (29, 18, 9, 3))
    return {
        EnemyKind.SCOUT: scout,
        EnemyKind.GUNSHIP: gunship,
        EnemyKind.BOMBER: bomber,
    }


def create_boss_surface() -> pygame.Surface:
    """Stvori veliki viktorijanski dreadnought sprite za ISS Goliath."""
    surface = pygame.Surface((150, 72), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, (34, 36, 40), (13, 3, 114, 25))
    pygame.draw.ellipse(surface, (87, 75, 56), (9, 1, 122, 28), 3)
    for x in (31, 52, 73, 94, 115):
        pygame.draw.arc(surface, (80, 72, 59), (x - 10, 4, 20, 23), 1.35, 4.95, 1)

    pygame.draw.rect(surface, (46, 40, 38), (18, 30, 110, 20), border_radius=3)
    pygame.draw.rect(surface, (111, 75, 44), (25, 35, 96, 9), border_radius=2)
    pygame.draw.rect(surface, BRASS, (29, 29, 88, 4), border_radius=2)
    pygame.draw.line(surface, BRIGHT_BRASS, (31, 49), (114, 49), 2)
    pygame.draw.polygon(surface, IRON, ((120, 27), (149, 40), (120, 53)))
    pygame.draw.polygon(surface, IRON, ((22, 27), (0, 40), (22, 53)))

    for x in (39, 63, 87, 111):
        pygame.draw.circle(surface, (177, 59, 52), (x, 41), 5)
        pygame.draw.circle(surface, (244, 177, 82), (x, 41), 2)
    _rivet_row(surface, 32, (34, 46, 58, 70, 82, 94, 106))
    _rivet_row(surface, 47, (32, 44, 56, 68, 80, 92, 104, 116))

    for x, height in ((50, 12), (74, 17), (98, 12)):
        pygame.draw.rect(surface, IRON, (x, 18 - height // 2, 7, height))
        pygame.draw.rect(surface, BRASS, (x - 2, 16 - height // 2, 11, 3))
    pygame.draw.circle(surface, AETHER, (75, 57), 7)
    pygame.draw.circle(surface, (232, 220, 181), (75, 57), 3)
    return surface


def create_repair_surface() -> pygame.Surface:
    """Stvori aether ćeliju s križem koja označava popravak."""
    surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(surface, (25, 58, 61), (16, 16), 14)
    pygame.draw.circle(surface, AETHER, (16, 16), 12, 3)
    pygame.draw.circle(surface, BRASS, (16, 16), 15, 1)
    pygame.draw.rect(surface, (231, 222, 179), (13, 7, 6, 18), border_radius=1)
    pygame.draw.rect(surface, (231, 222, 179), (7, 13, 18, 6), border_radius=1)
    pygame.draw.circle(surface, (226, 255, 198), (16, 16), 3)
    return surface
