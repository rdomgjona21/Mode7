"""Proceduralne slike projektila, trening-cilja i popravka."""

import pygame


def create_projectile_surfaces() -> dict[str, pygame.Surface]:
    """Stvori prepoznatljive slike za top, raspršenu paljbu i raketu."""
    cannon = pygame.Surface((12, 6), pygame.SRCALPHA)
    pygame.draw.ellipse(cannon, (236, 190, 83), cannon.get_rect())
    pygame.draw.circle(cannon, (255, 239, 168), (9, 3), 2)

    spread = pygame.Surface((10, 6), pygame.SRCALPHA)
    pygame.draw.polygon(spread, (62, 220, 225), ((0, 3), (7, 0), (10, 3), (7, 6)))

    rocket = pygame.Surface((18, 9), pygame.SRCALPHA)
    pygame.draw.polygon(rocket, (197, 76, 54), ((0, 1), (12, 1), (18, 4), (12, 8), (0, 8)))
    pygame.draw.polygon(rocket, (242, 187, 67), ((0, 2), (0, 7), (5, 4)))
    return {"cannon": cannon, "spread": spread, "rocket": rocket}


def create_training_target_surface() -> pygame.Surface:
    """Stvori jasan privremeni cilj s koncentričnim krugovima."""
    surface = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.circle(surface, (76, 53, 43), (24, 24), 22)
    pygame.draw.circle(surface, (205, 166, 82), (24, 24), 17, 4)
    pygame.draw.circle(surface, (185, 67, 54), (24, 24), 10)
    pygame.draw.circle(surface, (236, 219, 169), (24, 24), 4)
    return surface


def create_repair_surface() -> pygame.Surface:
    """Stvori cijan ćeliju s križem koja označava popravak."""
    surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(surface, (34, 73, 78), (16, 16), 14)
    pygame.draw.circle(surface, (65, 211, 202), (16, 16), 12, 3)
    pygame.draw.rect(surface, (231, 222, 179), (13, 7, 6, 18))
    pygame.draw.rect(surface, (231, 222, 179), (7, 13, 18, 6))
    return surface
