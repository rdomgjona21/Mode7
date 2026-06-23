"""Aplikacijska stanja izvan same borbene simulacije."""

from enum import StrEnum


class AppState(StrEnum):
    """Visokorazinska stanja PyGame aplikacije."""

    MAIN_MENU = "main_menu"
    INSTRUCTIONS = "instructions"
    PLAYING = "playing"
    PAUSED = "paused"
