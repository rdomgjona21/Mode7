"""Odabir oružja, hlađenja i stvaranje igrača projektila."""

import math
from dataclasses import dataclass
from enum import StrEnum

from aetherfront.gameplay.balance import CombatBalance, WeaponBalance
from aetherfront.gameplay.projectiles import Projectile


class PrimaryWeapon(StrEnum):
    """Dvije zamjenjive vrste primarnog oružja."""

    CANNON = "cannon"
    SPREAD = "spread"


@dataclass(slots=True)
class WeaponController:
    """Upravlja odabirom i neovisnim hlađenjem svih oružja."""

    cannon: WeaponBalance
    spread: WeaponBalance
    rocket: WeaponBalance
    primary: PrimaryWeapon = PrimaryWeapon.CANNON
    cannon_cooldown: float = 0.0
    spread_cooldown: float = 0.0
    rocket_cooldown: float = 0.0

    @classmethod
    def from_balance(cls, balance: CombatBalance) -> "WeaponController":
        """Stvori kontroler iz provjerene borbene konfiguracije."""
        return cls(cannon=balance.cannon, spread=balance.spread, rocket=balance.rocket)

    def update(self, dt: float) -> None:
        """Smanji sva hlađenja bez prelaska ispod nule."""
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("delta time must be finite and non-negative")
        self.cannon_cooldown = max(0.0, self.cannon_cooldown - dt)
        self.spread_cooldown = max(0.0, self.spread_cooldown - dt)
        self.rocket_cooldown = max(0.0, self.rocket_cooldown - dt)

    def select_primary(self, weapon: PrimaryWeapon) -> None:
        """Promijeni aktivno primarno oružje."""
        self.primary = weapon

    @property
    def primary_name(self) -> str:
        """Vrati engleski naziv prikladan za HUD."""
        return "CANNON" if self.primary is PrimaryWeapon.CANNON else "SPREAD GUN"

    @property
    def rocket_ready(self) -> bool:
        """Raketa je spremna kada joj je hlađenje završilo."""
        return self.rocket_cooldown <= 0

    def _create_projectiles(
        self,
        weapon: WeaponBalance,
        kind: str,
        x: float,
        y: float,
        heading: float,
    ) -> list[Projectile]:
        """Stvori konfigurirani uzorak projektila malo ispred igrača."""
        spawn_distance = 24.0
        spawn_x = x + math.cos(heading) * spawn_distance
        spawn_y = y + math.sin(heading) * spawn_distance
        return [
            Projectile(
                x=spawn_x,
                y=spawn_y,
                heading=heading + offset,
                speed=weapon.projectile_speed,
                damage=weapon.damage,
                radius=weapon.projectile_radius,
                lifetime_remaining=weapon.projectile_lifetime_seconds,
                team="player",
                kind=kind,
            )
            for offset in weapon.angle_offsets
        ]

    def fire_primary(
        self,
        x: float,
        y: float,
        heading: float,
        available_slots: int,
    ) -> list[Projectile]:
        """Pucaj aktivnim primarnim oružjem ako je spremno i ima mjesta."""
        if self.primary is PrimaryWeapon.CANNON:
            weapon = self.cannon
            cooldown = self.cannon_cooldown
        else:
            weapon = self.spread
            cooldown = self.spread_cooldown

        if cooldown > 0 or available_slots < len(weapon.angle_offsets):
            return []

        if self.primary is PrimaryWeapon.CANNON:
            self.cannon_cooldown = weapon.cooldown_seconds
        else:
            self.spread_cooldown = weapon.cooldown_seconds
        return self._create_projectiles(weapon, self.primary.value, x, y, heading)

    def fire_rocket(
        self,
        x: float,
        y: float,
        heading: float,
        available_slots: int,
    ) -> list[Projectile]:
        """Ispali raketu ako je spremna i postoji slobodno mjesto."""
        if self.rocket_cooldown > 0 or available_slots < 1:
            return []
        self.rocket_cooldown = self.rocket.cooldown_seconds
        return self._create_projectiles(self.rocket, "rocket", x, y, heading)
