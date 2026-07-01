"""Standardni protivnici: scout, gunship i bomber."""

import math
from dataclasses import dataclass
from enum import StrEnum

from aetherfront.config import WORLD_SIZE
from aetherfront.gameplay.balance import EnemyBalance
from aetherfront.gameplay.collisions import CircleBody, wrapped_axis_delta
from aetherfront.gameplay.projectiles import Projectile
from aetherfront.gameplay.validation import (
    require_all_finite,
    require_non_negative,
    require_positive,
)


class EnemyKind(StrEnum):
    """Zaključane standardne vrste protivnika za P5 vertikalni presjek."""

    SCOUT = "scout"
    GUNSHIP = "gunship"
    BOMBER = "bomber"


@dataclass(slots=True)
class Enemy:
    """Jedan neprijateljski zračni brod u omotanom svijetu."""

    kind: EnemyKind
    x: float
    y: float
    heading: float
    max_health: float
    speed: float
    radius: float
    score_value: int
    contact_damage: float
    projectile_damage: float
    attack_cooldown_seconds: float
    projectile_speed: float
    projectile_radius: float
    projectile_lifetime_seconds: float
    health: float | None = None
    attack_cooldown_remaining: float = 0.0
    strafe_phase: float = 0.0

    def __post_init__(self) -> None:
        """Odbij numerički neispravnog protivnika prije simulacije."""
        require_all_finite(
            (
                ("enemy x", self.x),
                ("enemy y", self.y),
                ("enemy heading", self.heading),
                ("enemy attack cooldown remaining", self.attack_cooldown_remaining),
                ("enemy strafe phase", self.strafe_phase),
            )
        )
        require_positive(self.max_health, "enemy health")
        require_positive(self.speed, "enemy speed")
        require_positive(self.radius, "enemy radius")
        if self.score_value <= 0:
            raise ValueError("enemy score value must be positive")
        require_positive(self.contact_damage, "enemy contact damage")
        require_positive(self.projectile_damage, "enemy projectile damage")
        require_positive(self.attack_cooldown_seconds, "enemy attack cooldown")
        require_positive(self.projectile_speed, "enemy projectile speed")
        require_positive(self.projectile_radius, "enemy projectile radius")
        require_positive(self.projectile_lifetime_seconds, "enemy projectile lifetime")
        self.heading %= math.tau
        if self.health is None:
            self.health = self.max_health
        else:
            require_non_negative(self.health, "enemy health")
        self.health = min(self.health, self.max_health)

    @classmethod
    def from_balance(
        cls,
        kind: EnemyKind,
        balance: EnemyBalance,
        x: float,
        y: float,
        heading: float = 0.0,
        attack_cooldown_remaining: float = 0.0,
    ) -> "Enemy":
        """Stvori protivnika iz provjerene konfiguracije balansa."""
        return cls(
            kind=kind,
            x=x % WORLD_SIZE,
            y=y % WORLD_SIZE,
            heading=heading,
            max_health=balance.max_health,
            speed=balance.speed,
            radius=balance.collision_radius,
            score_value=balance.score_value,
            contact_damage=balance.contact_damage,
            projectile_damage=balance.projectile_damage,
            attack_cooldown_seconds=balance.attack_cooldown_seconds,
            projectile_speed=balance.projectile_speed,
            projectile_radius=balance.projectile_radius,
            projectile_lifetime_seconds=balance.projectile_lifetime_seconds,
            attack_cooldown_remaining=attack_cooldown_remaining,
        )

    @property
    def alive(self) -> bool:
        """Protivnik je aktivan dok ima više od nule trupa."""
        return self.health is not None and self.health > 0

    @property
    def collision_body(self) -> CircleBody:
        """Vrati kružni oblik za sudare projektila, igrača i protivnika."""
        return CircleBody(self.x, self.y, self.radius)

    @property
    def projectile_kind(self) -> str:
        """Vrsta neprijateljskog projektila za izbor proceduralnog spritea."""
        if self.kind is EnemyKind.BOMBER:
            return "enemy_heavy"
        return "enemy_light"

    def take_damage(self, amount: float) -> bool:
        """Primijeni štetu i vrati je li ovaj pogodak uništio protivnika."""
        if not math.isfinite(amount) or amount < 0:
            raise ValueError("damage must be finite and non-negative")
        if not self.alive or amount == 0:
            return False
        assert self.health is not None
        self.health = max(0.0, self.health - amount)
        return not self.alive

    def _heading_toward(self, player_x: float, player_y: float) -> float:
        delta_x = wrapped_axis_delta(self.x, player_x)
        delta_y = wrapped_axis_delta(self.y, player_y)
        return math.atan2(delta_y, delta_x) % math.tau

    def _desired_heading(self, player_x: float, player_y: float) -> float:
        base = self._heading_toward(player_x, player_y)
        if self.kind is EnemyKind.SCOUT:
            return (base + math.sin(self.strafe_phase) * 0.55) % math.tau
        if self.kind is EnemyKind.GUNSHIP:
            return (base + math.sin(self.strafe_phase) * 0.25) % math.tau
        return base

    def update(self, dt: float, player_x: float, player_y: float) -> None:
        """Pomakni protivnika i odbroji napad neovisno o broju frameova."""
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("delta time must be finite and non-negative")
        if not self.alive:
            return

        self.strafe_phase += dt * {
            EnemyKind.SCOUT: 5.0,
            EnemyKind.GUNSHIP: 2.6,
            EnemyKind.BOMBER: 1.4,
        }[self.kind]
        self.heading = self._desired_heading(player_x, player_y)
        self.x = (self.x + math.cos(self.heading) * self.speed * dt) % WORLD_SIZE
        self.y = (self.y + math.sin(self.heading) * self.speed * dt) % WORLD_SIZE
        self.attack_cooldown_remaining = max(0.0, self.attack_cooldown_remaining - dt)

    def fire_if_ready(self, player_x: float, player_y: float) -> Projectile | None:
        """Stvori neprijateljski projektil ako je hlađenje završeno."""
        if not self.alive or self.attack_cooldown_remaining > 0:
            return None
        heading = self._heading_toward(player_x, player_y)
        self.attack_cooldown_remaining = self.attack_cooldown_seconds
        return Projectile(
            x=self.x,
            y=self.y,
            heading=heading,
            speed=self.projectile_speed,
            damage=self.projectile_damage,
            radius=self.projectile_radius,
            lifetime_remaining=self.projectile_lifetime_seconds,
            team="enemy",
            kind=self.projectile_kind,
        )
