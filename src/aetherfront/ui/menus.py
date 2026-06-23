"""Engleski ekrani izbornika, uputa, pauze i završetka pokušaja."""

import pygame

from aetherfront.config import INTERNAL_SIZE
from aetherfront.gameplay.session import CombatSession

PANEL_COLOR = (12, 18, 28, 218)
TEXT_COLOR = (232, 220, 181)
ACCENT_COLOR = (67, 193, 169)
DANGER_COLOR = (193, 63, 57)
SHADOW_COLOR = (8, 11, 17)


def _label(
    canvas: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    center: tuple[int, int],
    color: tuple[int, int, int] = TEXT_COLOR,
) -> None:
    """Nacrtaj centrirani tekst s malom sjenom radi čitljivosti."""
    shadow = font.render(text, True, SHADOW_COLOR)
    foreground = font.render(text, True, color)
    shadow_rect = shadow.get_rect(center=(center[0] + 1, center[1] + 1))
    foreground_rect = foreground.get_rect(center=center)
    canvas.blit(shadow, shadow_rect)
    canvas.blit(foreground, foreground_rect)


def _panel(canvas: pygame.Surface) -> None:
    panel = pygame.Surface((500, 258), pygame.SRCALPHA)
    panel.fill(PANEL_COLOR)
    rect = panel.get_rect(center=(INTERNAL_SIZE[0] // 2, INTERNAL_SIZE[1] // 2))
    canvas.blit(panel, rect)
    pygame.draw.rect(canvas, (222, 205, 158), rect, 1)


def draw_main_menu(canvas: pygame.Surface, font: pygame.font.Font) -> None:
    """Nacrtaj početni izbornik igre."""
    _panel(canvas)
    _label(canvas, font, "AETHERFRONT: ZEPPELIN WARS", (320, 86), ACCENT_COLOR)
    _label(canvas, font, "Siege of Brasshaven", (320, 124))
    _label(canvas, font, "Destroy three waves and the ISS Goliath.", (320, 158))
    _label(canvas, font, "ENTER / SPACE  Start Mission", (320, 206))
    _label(canvas, font, "I  Instructions", (320, 230))
    _label(canvas, font, "ESC  Quit", (320, 254))


def draw_instructions(canvas: pygame.Surface, font: pygame.font.Font) -> None:
    """Nacrtaj kratke upute prije početka borbe."""
    _panel(canvas)
    _label(canvas, font, "MISSION BRIEFING", (320, 74), ACCENT_COLOR)
    _label(canvas, font, "A/D or Arrows: steer", (320, 108))
    _label(canvas, font, "W/S or Arrows: throttle", (320, 132))
    _label(canvas, font, "1/2: switch weapon   Space: fire", (320, 156))
    _label(canvas, font, "Shift: rocket   Esc: pause", (320, 180))
    _label(canvas, font, "Survive, repair, then sink the dreadnought.", (320, 214))
    _label(canvas, font, "ENTER / SPACE  Start   M  Main Menu", (320, 252))


def draw_pause_menu(canvas: pygame.Surface, font: pygame.font.Font) -> None:
    """Nacrtaj pauzni izbornik preko zamrznute igre."""
    _panel(canvas)
    _label(canvas, font, "PAUSED", (320, 108), ACCENT_COLOR)
    _label(canvas, font, "ESC  Resume", (320, 154))
    _label(canvas, font, "R  Restart Mission", (320, 186))
    _label(canvas, font, "M  Main Menu", (320, 218))


def draw_terminal_menu(
    canvas: pygame.Surface,
    font: pygame.font.Font,
    session: CombatSession,
) -> None:
    """Nacrtaj završni ekran nakon pobjede ili poraza."""
    if not session.victory and not session.game_over:
        return

    _panel(canvas)
    if session.victory:
        title = "VICTORY"
        subtitle = "Brasshaven holds."
        color = ACCENT_COLOR
    else:
        title = "GAME OVER"
        subtitle = "The Kestrel is lost."
        color = DANGER_COLOR

    _label(canvas, font, title, (320, 104), color)
    _label(canvas, font, subtitle, (320, 142))
    _label(canvas, font, f"Final score: {session.score:05d}", (320, 180))
    _label(canvas, font, "R  Retry Mission", (320, 222))
    _label(canvas, font, "M  Main Menu", (320, 248))
