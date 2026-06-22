"""Učitavanje i provjera vrijednosti borbenog balansa iz JSON datoteke."""

import json
import math
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class PlayerBalance:
    """Početne vrijednosti zdravlja i sudara igrača."""

    max_health: float
    collision_radius: float
    invulnerability_seconds: float


@dataclass(frozen=True, slots=True)
class ProjectileBalance:
    """Zajedničke zadane vrijednosti budućih projektila."""

    collision_radius: float
    lifetime_seconds: float


@dataclass(frozen=True, slots=True)
class CombatBalance:
    """Provjerena borbena konfiguracija dostupna ostatku igre."""

    player: PlayerBalance
    projectile: ProjectileBalance


def _positive_number(section: dict[str, Any], key: str, section_name: str) -> float:
    """Dohvati konačan pozitivan broj ili prijavi njegov točan položaj u JSON-u."""
    value = section.get(key)
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{section_name}.{key} must be a positive number")
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise ValueError(f"{section_name}.{key} must be a positive number")
    return result


def _section(data: dict[str, Any], name: str) -> dict[str, Any]:
    """Dohvati obvezni objekt konfiguracije."""
    value = data.get(name)
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def load_combat_balance(path: Path | None = None) -> CombatBalance:
    """Učitaj zadanu paketnu konfiguraciju ili datoteku poslanu iz testa."""
    if path is None:
        resource = files("aetherfront").joinpath("data/balance.json")
        with resource.open(encoding="utf-8") as handle:
            raw = json.load(handle)
    else:
        with path.open(encoding="utf-8") as handle:
            raw = json.load(handle)

    if not isinstance(raw, dict):
        raise ValueError("balance root must be an object")

    player = _section(raw, "player")
    projectile = _section(raw, "projectile")
    return CombatBalance(
        player=PlayerBalance(
            max_health=_positive_number(player, "max_health", "player"),
            collision_radius=_positive_number(player, "collision_radius", "player"),
            invulnerability_seconds=_positive_number(
                player,
                "invulnerability_seconds",
                "player",
            ),
        ),
        projectile=ProjectileBalance(
            collision_radius=_positive_number(
                projectile,
                "collision_radius",
                "projectile",
            ),
            lifetime_seconds=_positive_number(
                projectile,
                "lifetime_seconds",
                "projectile",
            ),
        ),
    )
