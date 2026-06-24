"""Proceduralni prikazi zračnih brodova bez vanjskih slikovnih datoteka."""

import pygame


def create_kestrel_surface() -> pygame.Surface:
    """Stvori transparentan viktorijanski prikaz igračevog broda Kestrel."""
    surface = pygame.Surface((96, 64), pygame.SRCALPHA)

    brass = (204, 158, 72)
    bright_brass = (236, 203, 123)
    dark_wood = (75, 52, 38)
    warm_wood = (151, 101, 53)
    canvas = (120, 132, 123)
    canvas_light = (169, 179, 159)
    iron = (39, 44, 50)
    aether = (56, 211, 215)

    # Stražnji aether plamen i mjedeni ispuh stvaraju dojam stalnog pogona.
    pygame.draw.polygon(
        surface,
        (aether[0], aether[1], aether[2], 145),
        ((6, 34), (24, 25), (24, 43)),
    )
    pygame.draw.polygon(surface, (239, 179, 68, 225), ((14, 34), (30, 29), (30, 39)))
    pygame.draw.rect(surface, iron, (25, 30, 7, 8), border_radius=2)

    # Veliki platneni balon i rebra daju viktorijanski zračni profil.
    pygame.draw.ellipse(surface, (61, 75, 77), (15, 3, 70, 30))
    pygame.draw.ellipse(surface, canvas, (18, 5, 64, 26))
    pygame.draw.ellipse(surface, canvas_light, (24, 8, 52, 14))
    for x in (28, 42, 56, 70):
        pygame.draw.arc(surface, (78, 93, 92), (x - 8, 5, 16, 26), 1.45, 4.85, 1)
    pygame.draw.line(surface, bright_brass, (22, 20), (78, 20), 1)

    # Nosači povezuju balon s gondolom.
    struts = (
        ((27, 29), (34, 42)),
        ((42, 31), (43, 42)),
        ((61, 31), (57, 42)),
        ((76, 28), (68, 42)),
    )
    for start, end in struts:
        pygame.draw.line(surface, brass, start, end, 2)

    # Drvena gondola s mjedenim pramcem i krmom.
    pygame.draw.polygon(
        surface,
        dark_wood,
        ((23, 41), (72, 41), (87, 47), (72, 56), (31, 56), (13, 48)),
    )
    pygame.draw.polygon(
        surface,
        warm_wood,
        ((29, 42), (70, 42), (78, 47), (66, 52), (33, 52), (21, 48)),
    )
    pygame.draw.polygon(surface, bright_brass, ((72, 42), (94, 47), (72, 52)))
    pygame.draw.polygon(surface, brass, ((19, 45), (4, 49), (20, 53)))
    pygame.draw.line(surface, bright_brass, (28, 44), (70, 44), 2)
    pygame.draw.line(surface, (97, 64, 40), (31, 53), (66, 53), 2)

    # Kabina, prozori, zakovice i peraje čine brod čitljivim u maloj rezoluciji.
    pygame.draw.ellipse(surface, (36, 166, 177), (44, 36, 17, 11))
    pygame.draw.ellipse(surface, (226, 244, 210), (49, 39, 7, 5))
    for x in (33, 42, 61, 70):
        pygame.draw.circle(surface, bright_brass, (x, 47), 2)
    pygame.draw.polygon(surface, (96, 63, 40), ((31, 52), (21, 62), (43, 54)))
    pygame.draw.polygon(surface, (96, 63, 40), ((66, 52), (77, 62), (56, 54)))
    pygame.draw.circle(surface, aether, (51, 47), 4)

    # Mali dimnjak daje prepoznatljiv steampunk detalj bez novog efektnog sustava.
    pygame.draw.rect(surface, iron, (61, 33, 5, 9))
    pygame.draw.rect(surface, brass, (59, 31, 9, 3))

    return surface
