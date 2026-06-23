"""Osnovni engleski HUD za borbu protiv standardnih protivnika."""

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
    """Nacrtaj zdravlje, oružje, val, bodove, neprijatelje, brzinu i FPS."""
    panel = pygame.Surface((252, 150), pygame.SRCALPHA)
    panel.fill((14, 22, 31, 174))
    canvas.blit(panel, (8, 8))

    health_ratio = session.player.health / session.player.max_health
    pygame.draw.rect(canvas, (79, 45, 43), (18, 27, 150, 10))
    pygame.draw.rect(canvas, (67, 193, 169), (18, 27, round(150 * health_ratio), 10))
    pygame.draw.rect(canvas, (222, 205, 158), (18, 27, 150, 10), 1)

    hull = f"HULL {session.player.health:.0f}/{session.player.max_health:.0f}"
    _label(canvas, font, hull, (18, 11))
    _label(canvas, font, f"WEAPON {session.weapons.primary_name}", (18, 44))
    rocket = "READY" if session.weapons.rocket_ready else f"{session.weapons.rocket_cooldown:.1f}s"
    _label(canvas, font, f"ROCKET {rocket}", (18, 60))
    _label(canvas, font, f"SCORE {session.score:05d}", (18, 76))

    director = session.wave_director
    if director.waves_complete:
        wave = "WAVES CLEAR"
    elif director.incoming:
        wave = f"INCOMING {director.intermission_remaining:.1f}s"
    else:
        wave = f"WAVE {director.current_wave_number}/{director.total_waves}"
    _label(canvas, font, wave, (18, 92))

    threat = session.lowest_health_enemy
    if threat is not None:
        enemy = f"{threat.kind.value.upper()} {threat.health:.0f}/{threat.max_health:.0f}"
    else:
        enemy = director.current_wave_name.upper()
    _label(canvas, font, f"ENEMIES {session.enemies_remaining}  {enemy}", (18, 108))

    if session.boss is not None:
        boss = session.boss
        boss_ratio = 0.0 if boss.health is None else boss.health / boss.max_health
        _label(canvas, font, f"BOSS GOLIATH {boss.phase_label}", (18, 124))
        pygame.draw.rect(canvas, (79, 45, 43), (18, 143, 210, 6))
        pygame.draw.rect(canvas, (193, 63, 57), (18, 143, round(210 * boss_ratio), 6))
        pygame.draw.rect(canvas, (222, 205, 158), (18, 143, 210, 6), 1)
    if session.victory:
        _label(canvas, font, "VICTORY - BRASSHAVEN HOLDS", (182, 172))
    elif session.game_over:
        _label(canvas, font, "GAME OVER - KESTREL LOST", (182, 172))
    _label(canvas, font, f"SPEED {speed:04.1f}   FPS {fps:04.1f}", (466, 11))
