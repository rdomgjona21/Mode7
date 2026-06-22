"""Proceduralni prikazi zračnih brodova bez vanjskih slikovnih datoteka."""

import pygame


def create_kestrel_surface() -> pygame.Surface:
    """Stvori transparentan prikaz igračevog broda Kestrel veličine 96×64."""
    surface = pygame.Surface((96, 64), pygame.SRCALPHA)

    # Stražnji plamen ostaje iza trupa i daje dojam stalnog pogona.
    pygame.draw.polygon(surface, (70, 214, 226, 150), ((9, 32), (24, 25), (24, 39)))
    pygame.draw.polygon(surface, (235, 184, 72, 220), ((15, 32), (28, 28), (28, 36)))

    # Balon i metalni trup koriste zaključanu olujno-plavu i mjedenu paletu.
    pygame.draw.ellipse(surface, (63, 82, 96), (17, 6, 68, 27))
    pygame.draw.ellipse(surface, (126, 145, 151), (22, 9, 58, 18))
    pygame.draw.line(surface, (201, 166, 91), (26, 30), (31, 42), 2)
    pygame.draw.line(surface, (201, 166, 91), (70, 30), (65, 42), 2)
    pygame.draw.polygon(
        surface,
        (74, 57, 45),
        ((25, 40), (74, 40), (86, 47), (70, 55), (31, 55), (15, 47)),
    )
    pygame.draw.polygon(
        surface,
        (165, 124, 63),
        ((29, 41), (70, 41), (78, 47), (66, 51), (33, 51), (21, 47)),
    )

    # Kabina, pramac i peraje čine siluetu čitljivom i bez oslanjanja samo na boju.
    pygame.draw.ellipse(surface, (48, 185, 193), (44, 37, 15, 10))
    pygame.draw.polygon(surface, (207, 170, 92), ((74, 43), (93, 47), (74, 51)))
    pygame.draw.polygon(surface, (108, 75, 48), ((30, 50), (20, 61), (42, 53)))
    pygame.draw.polygon(surface, (108, 75, 48), ((66, 50), (76, 61), (55, 53)))
    pygame.draw.circle(surface, (230, 218, 178), (51, 42), 2)

    return surface
