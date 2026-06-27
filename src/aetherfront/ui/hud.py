"""Minimalistički steampunk HUD za borbu."""

import pygame

from aetherfront.gameplay.session import CombatSession

HUD_RECT = pygame.Rect(8, 8, 624, 30)
HEALTH_BAR_RECT = pygame.Rect(18, 28, 104, 6)
BOSS_BAR_RECT = pygame.Rect(384, 28, 116, 6)
BRASS = (198, 151, 72)
BRIGHT_BRASS = (235, 210, 143)
PANEL_FILL = (12, 19, 27, 184)
PANEL_LINE = (92, 68, 42)
TEXT = (232, 220, 181)
SHADOW = (13, 19, 25)
AETHER = (67, 193, 169)
DAMAGE = (89, 45, 42)
BOSS_RED = (193, 63, 57)


def format_elapsed_time(seconds: float) -> str:
    """Vrati vrijeme sesije u engleskom HUD formatu MM:SS."""
    total_seconds = max(0, int(seconds))
    minutes, seconds_remainder = divmod(total_seconds, 60)
    return f"{minutes:02d}:{seconds_remainder:02d}"


def _label(
    canvas: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    position: tuple[int, int],
) -> None:
    shadow = font.render(text, True, SHADOW)
    foreground = font.render(text, True, TEXT)
    canvas.blit(shadow, (position[0] + 1, position[1] + 1))
    canvas.blit(foreground, position)


def _panel(canvas: pygame.Surface, rect: pygame.Rect) -> None:
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    panel.fill(PANEL_FILL)
    canvas.blit(panel, rect.topleft)
    pygame.draw.rect(canvas, PANEL_LINE, rect, 1)
    pygame.draw.line(canvas, BRASS, rect.topleft, (rect.left + 26, rect.top), 2)
    pygame.draw.line(canvas, BRASS, rect.topleft, (rect.left, rect.top + 26), 2)
    pygame.draw.line(canvas, BRASS, rect.topright, (rect.right - 27, rect.top), 2)
    pygame.draw.line(canvas, BRASS, rect.topright, (rect.right - 1, rect.top + 26), 2)
    for point in (
        (rect.left + 7, rect.top + 7),
        (rect.right - 8, rect.top + 7),
        (rect.left + 7, rect.bottom - 8),
        (rect.right - 8, rect.bottom - 8),
    ):
        pygame.draw.circle(canvas, BRIGHT_BRASS, point, 2)


def _bar(
    canvas: pygame.Surface,
    rect: pygame.Rect,
    ratio: float,
    fill: tuple[int, int, int],
) -> None:
    clamped = max(0.0, min(1.0, ratio))
    pygame.draw.rect(canvas, DAMAGE, rect)
    pygame.draw.rect(
        canvas,
        fill,
        (rect.x, rect.y, round(rect.width * clamped), rect.height),
    )
    pygame.draw.rect(canvas, BRIGHT_BRASS, rect, 1)
    for tick in range(1, 5):
        x = rect.x + tick * rect.width // 5
        pygame.draw.line(canvas, PANEL_LINE, (x, rect.y + 1), (x, rect.bottom - 2))


def _vertical_separator(canvas: pygame.Surface, x: int) -> None:
    pygame.draw.line(canvas, PANEL_LINE, (x, HUD_RECT.top + 6), (x, HUD_RECT.bottom - 6))
    pygame.draw.line(
        canvas,
        (44, 35, 27),
        (x + 1, HUD_RECT.top + 6),
        (x + 1, HUD_RECT.bottom - 6),
    )


def _wave_text(session: CombatSession) -> str:
    director = session.wave_director
    if director.waves_complete:
        return "CLEAR"
    if director.incoming:
        return f"IN {director.intermission_remaining:.1f}s"
    return f"WAVE {director.current_wave_number}/{director.total_waves}"


def _enemy_text(session: CombatSession) -> str:
    threat = session.lowest_health_enemy
    if threat is not None:
        enemy = f"{threat.kind.value.upper()} {threat.health:.0f}/{threat.max_health:.0f}"
    else:
        enemy = session.wave_director.current_wave_name.upper()
    return f"EN {session.enemies_remaining} {enemy}"


def draw_hud(
    canvas: pygame.Surface,
    font: pygame.font.Font,
    session: CombatSession,
    speed: float,
    fps: float,
) -> None:
    """Nacrtaj zdravlje, oružje, val, bodove, neprijatelje, brzinu i FPS."""
    _panel(canvas, HUD_RECT)

    health_ratio = session.player.health / session.player.max_health

    hull = f"HULL {session.player.health:.0f}/{session.player.max_health:.0f}"
    _label(canvas, font, hull, (18, 12))
    _bar(canvas, HEALTH_BAR_RECT, health_ratio, AETHER)
    _vertical_separator(canvas, 132)

    _label(canvas, font, f"WPN {session.weapons.primary_name}", (144, 12))
    rocket = "READY" if session.weapons.rocket_ready else f"{session.weapons.rocket_cooldown:.1f}s"
    _label(canvas, font, f"RKT {rocket}", (144, 25))
    _vertical_separator(canvas, 252)

    _label(canvas, font, f"SCORE {session.score:05d}", (264, 12))
    _label(canvas, font, f"TIME {format_elapsed_time(session.elapsed_time)}", (264, 25))
    _vertical_separator(canvas, 374)

    _label(canvas, font, _wave_text(session), (386, 12))

    if session.boss is not None:
        boss = session.boss
        boss_ratio = 0.0 if boss.health is None else boss.health / boss.max_health
        _label(canvas, font, f"BOSS {boss.phase_label}", (506, 12))
        _bar(canvas, BOSS_BAR_RECT, boss_ratio, BOSS_RED)
    else:
        _label(canvas, font, _enemy_text(session), (386, 25))

    _label(canvas, font, f"SPD {speed:04.1f}", (514, 25))
    _label(canvas, font, f"FPS {fps:04.1f}", (574, 25))

    if session.victory:
        _label(canvas, font, "VICTORY - BRASSHAVEN HOLDS", (182, 172))
    elif session.game_over:
        _label(canvas, font, "GAME OVER - KESTREL LOST", (182, 172))
