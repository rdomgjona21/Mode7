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
    limit: int


@dataclass(frozen=True, slots=True)
class WeaponBalance:
    """Vrijednosti jednog oružja i projektila koje stvara."""

    damage: float
    cooldown_seconds: float
    projectile_speed: float
    projectile_radius: float
    projectile_lifetime_seconds: float
    angle_offsets: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class RepairBalance:
    """Vrijednosti popravka koji ostaje nakon uništenog cilja."""

    heal_amount: float
    score_value: int
    collision_radius: float
    lifetime_seconds: float


@dataclass(frozen=True, slots=True)
class EnemyBalance:
    """Vrijednosti jedne standardne vrste protivnika."""

    max_health: float
    speed: float
    collision_radius: float
    score_value: int
    contact_damage: float
    projectile_damage: float
    attack_cooldown_seconds: float
    projectile_speed: float
    projectile_radius: float
    projectile_lifetime_seconds: float


@dataclass(frozen=True, slots=True)
class CombatBalance:
    """Provjerena borbena konfiguracija dostupna ostatku igre."""

    player: PlayerBalance
    projectile: ProjectileBalance
    cannon: WeaponBalance
    spread: WeaponBalance
    rocket: WeaponBalance
    repair: RepairBalance
    enemies: dict[str, EnemyBalance]


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


def _positive_integer(section: dict[str, Any], key: str, section_name: str) -> int:
    """Dohvati strogo pozitivan cijeli broj."""
    value = section.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{section_name}.{key} must be a positive integer")
    return value


def _angle_offsets(section: dict[str, Any], section_name: str) -> tuple[float, ...]:
    """Učitaj neprazan popis konačnih kutnih otklona."""
    raw = section.get("angle_offsets")
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"{section_name}.angle_offsets must be a non-empty array")
    offsets: list[float] = []
    for value in raw:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"{section_name}.angle_offsets must contain finite numbers")
        offset = float(value)
        if not math.isfinite(offset):
            raise ValueError(f"{section_name}.angle_offsets must contain finite numbers")
        offsets.append(offset)
    return tuple(offsets)


def _weapon(section: dict[str, Any], name: str) -> WeaponBalance:
    """Pretvori jednu JSON sekciju oružja u provjerenu konfiguraciju."""
    return WeaponBalance(
        damage=_positive_number(section, "damage", name),
        cooldown_seconds=_positive_number(section, "cooldown_seconds", name),
        projectile_speed=_positive_number(section, "projectile_speed", name),
        projectile_radius=_positive_number(section, "projectile_radius", name),
        projectile_lifetime_seconds=_positive_number(
            section,
            "projectile_lifetime_seconds",
            name,
        ),
        angle_offsets=_angle_offsets(section, name),
    )


def _enemy(section: dict[str, Any], name: str) -> EnemyBalance:
    """Pretvori jednu JSON sekciju protivnika u provjerenu konfiguraciju."""
    return EnemyBalance(
        max_health=_positive_number(section, "max_health", name),
        speed=_positive_number(section, "speed", name),
        collision_radius=_positive_number(section, "collision_radius", name),
        score_value=_positive_integer(section, "score_value", name),
        contact_damage=_positive_number(section, "contact_damage", name),
        projectile_damage=_positive_number(section, "projectile_damage", name),
        attack_cooldown_seconds=_positive_number(
            section,
            "attack_cooldown_seconds",
            name,
        ),
        projectile_speed=_positive_number(section, "projectile_speed", name),
        projectile_radius=_positive_number(section, "projectile_radius", name),
        projectile_lifetime_seconds=_positive_number(
            section,
            "projectile_lifetime_seconds",
            name,
        ),
    )


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
    weapons = _section(raw, "weapons")
    cannon = _section(weapons, "cannon")
    spread = _section(weapons, "spread")
    rocket = _section(weapons, "rocket")
    repair = _section(raw, "repair")
    enemies = _section(raw, "enemies")
    scout = _section(enemies, "scout")
    gunship = _section(enemies, "gunship")
    bomber = _section(enemies, "bomber")
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
            limit=_positive_integer(projectile, "limit", "projectile"),
        ),
        cannon=_weapon(cannon, "weapons.cannon"),
        spread=_weapon(spread, "weapons.spread"),
        rocket=_weapon(rocket, "weapons.rocket"),
        repair=RepairBalance(
            heal_amount=_positive_number(repair, "heal_amount", "repair"),
            score_value=_positive_integer(repair, "score_value", "repair"),
            collision_radius=_positive_number(repair, "collision_radius", "repair"),
            lifetime_seconds=_positive_number(repair, "lifetime_seconds", "repair"),
        ),
        enemies={
            "scout": _enemy(scout, "enemies.scout"),
            "gunship": _enemy(gunship, "enemies.gunship"),
            "bomber": _enemy(bomber, "enemies.bomber"),
        },
    )
