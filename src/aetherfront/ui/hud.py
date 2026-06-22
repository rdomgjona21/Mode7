"""Osnovni engleski HUD za trening-borbu."""

import pygame

from aetherfront.gameplay.session import CombatSession


def _label(
    canvas: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    position: tuple[int, int],
) -> None:
    shadow = font.render(text, True, (18, 25, 34))
    foreground = font.render(text, True, (232, 220, 181))
    canvas.blit(shadow, (position[0] + 1, position[1] + 1))
    canvas.blit(foreground, position)


def draw_hud(
    canvas: pygame.Surface,
    font: pygame.font.Font,
    session: CombatSession,
    speed: float,
    fps: float,
) -> None:
    """Nacrtaj zdravlje, oružje, raketu, bodove, cilj, brzinu i FPS."""
    panel = pygame.Surface((244, 118), pygame.SRCALPHA)
    panel.fill((14, 22, 31, 190))
    canvas.blit(panel, (8, 8))

    health_ratio = session.player.health / session.player.max_health
    pygame.draw.rect(canvas, (79, 45, 43), (18, 31, 170, 12))
    pygame.draw.rect(canvas, (67, 193, 169), (18, 31, round(170 * health_ratio), 12))
    pygame.draw.rect(canvas, (222, 205, 158), (18, 31, 170, 12), 1)

    hull = f"HULL {session.player.health:.0f}/{session.player.max_health:.0f}"
    _label(canvas, font, hull, (18, 13))
    _label(canvas, font, f"WEAPON {session.weapons.primary_name}", (18, 49))
    rocket = "READY" if session.weapons.rocket_ready else f"{session.weapons.rocket_cooldown:.1f}s"
    _label(canvas, font, f"ROCKET {rocket}", (18, 68))
    _label(canvas, font, f"SCORE {session.score:05d}", (18, 87))

    if session.target.alive:
        target = f"TARGET {session.target.health:.0f}/{session.target.max_health:.0f}"
    else:
        target = f"TARGET RESPAWN {session.target_respawn_remaining:.1f}s"
    _label(canvas, font, target, (18, 106))
    _label(canvas, font, f"SPEED {speed:04.1f}   FPS {fps:04.1f}", (450, 13))
