"""ISS Goliath dreadnought boss s dvije faze napada."""

import math
from dataclasses import dataclass
from enum import StrEnum

from aetherfront.config import WORLD_SIZE
from aetherfront.gameplay.balance import BossBalance
from aetherfront.gameplay.collisions import CircleBody, wrapped_axis_delta
from aetherfront.gameplay.projectiles import Projectile
from aetherfront.rendering.camera import Camera

BOSS_SPAWN_DISTANCE = 820.0
BOSS_MIN_FRONT_DEPTH = 420.0
BOSS_RECENTER_DISTANCE = 780.0


class BossPhase(StrEnum):
    """Faze ISS Goliatha."""

    PHASE_ONE = "phase_one"
    PHASE_TWO = "phase_two"
    DESTROYED = "destroyed"


@dataclass(slots=True)
class DreadnoughtBoss:
    """Veliki dreadnought koji se pojavljuje nakon tri redovna vala."""

    x: float
    y: float
    heading: float
    max_health: float
    radius: float
    score_value: int
    contact_damage: float
    phase_two_threshold: float
    phase_one_cooldown_seconds: float
    phase_two_cooldown_seconds: float
    projectile_damage: float
    projectile_speed: float
    projectile_radius: float
    projectile_lifetime_seconds: float
    health: float | None = None
    attack_cooldown_remaining: float = 0.8

    def __post_init__(self) -> None:
        """Provjeri osnovne vrijednosti prije uporabe u simulaciji."""
        numeric_values = (
            self.x,
            self.y,
            self.heading,
            self.max_health,
            self.radius,
            self.contact_damage,
            self.phase_two_threshold,
            self.phase_one_cooldown_seconds,
            self.phase_two_cooldown_seconds,
            self.projectile_damage,
            self.projectile_speed,
            self.projectile_radius,
            self.projectile_lifetime_seconds,
            self.attack_cooldown_remaining,
        )
        if not all(math.isfinite(value) for value in numeric_values):
            raise ValueError("boss values must be finite")
        if self.max_health <= 0 or self.radius <= 0:
            raise ValueError("boss health and radius must be positive")
        if self.score_value <= 0:
            raise ValueError("boss score value must be positive")
        if self.contact_damage <= 0 or self.projectile_damage <= 0:
            raise ValueError("boss damage values must be positive")
        if not 0 < self.phase_two_threshold < 1:
            raise ValueError("boss phase threshold must be between 0 and 1")
        if self.phase_one_cooldown_seconds <= 0 or self.phase_two_cooldown_seconds <= 0:
            raise ValueError("boss cooldown values must be positive")
        if self.projectile_speed <= 0 or self.projectile_radius <= 0:
            raise ValueError("boss projectile speed and radius must be positive")
        if self.projectile_lifetime_seconds <= 0:
            raise ValueError("boss projectile lifetime must be positive")
        self.heading %= math.tau
        if self.health is None:
            self.health = self.max_health
        elif not math.isfinite(self.health) or self.health < 0:
            raise ValueError("boss health must be finite and non-negative")
        self.health = min(self.health, self.max_health)

    @classmethod
    def spawn_ahead(cls, camera: Camera, balance: BossBalance) -> "DreadnoughtBoss":
        """Postavi Goliath daleko ispred trenutačnog smjera igrača."""
        return cls(
            x=(camera.x + math.cos(camera.heading) * BOSS_SPAWN_DISTANCE) % WORLD_SIZE,
            y=(camera.y + math.sin(camera.heading) * BOSS_SPAWN_DISTANCE) % WORLD_SIZE,
            heading=(camera.heading + math.pi) % math.tau,
            max_health=balance.max_health,
            radius=balance.collision_radius,
            score_value=balance.score_value,
            contact_damage=balance.contact_damage,
            phase_two_threshold=balance.phase_two_threshold,
            phase_one_cooldown_seconds=balance.phase_one_cooldown_seconds,
            phase_two_cooldown_seconds=balance.phase_two_cooldown_seconds,
            projectile_damage=balance.projectile_damage,
            projectile_speed=balance.projectile_speed,
            projectile_radius=balance.projectile_radius,
            projectile_lifetime_seconds=balance.projectile_lifetime_seconds,
        )

    @property
    def alive(self) -> bool:
        """Je li boss još aktivan."""
        return self.health is not None and self.health > 0

    @property
    def phase(self) -> BossPhase:
        """Odredi fazu iz preostalog zdravlja."""
        if not self.alive:
            return BossPhase.DESTROYED
        assert self.health is not None
        if self.health <= self.max_health * self.phase_two_threshold:
            return BossPhase.PHASE_TWO
        return BossPhase.PHASE_ONE

    @property
    def phase_label(self) -> str:
        """Kratka oznaka faze za HUD."""
        if self.phase is BossPhase.PHASE_TWO:
            return "PHASE 2"
        if self.phase is BossPhase.DESTROYED:
            return "DESTROYED"
        return "PHASE 1"

    @property
    def collision_body(self) -> CircleBody:
        """Kružni sudar velikog broda."""
        return CircleBody(self.x, self.y, self.radius)

    @property
    def current_cooldown_seconds(self) -> float:
        """Trenutačno vrijeme hlađenja ovisno o fazi."""
        if self.phase is BossPhase.PHASE_TWO:
            return self.phase_two_cooldown_seconds
        return self.phase_one_cooldown_seconds

    @property
    def burst_offsets(self) -> tuple[float, ...]:
        """Kutni otkloni projektila u trenutačnoj fazi."""
        if self.phase is BossPhase.PHASE_TWO:
            return (-0.28, -0.14, 0.0, 0.14, 0.28)
        return (-0.14, 0.0, 0.14)

    def take_damage(self, amount: float) -> bool:
        """Primijeni štetu i vrati je li ovaj pogodak uništio Goliath."""
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

    def update(self, dt: float, camera: Camera) -> None:
        """Održava boss u prednjem sektoru i odbrojava napad."""
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("delta time must be finite and non-negative")
        if not self.alive:
            return

        forward_x = math.cos(camera.heading)
        forward_y = math.sin(camera.heading)
        delta_x = wrapped_axis_delta(camera.x, self.x)
        delta_y = wrapped_axis_delta(camera.y, self.y)
        depth = delta_x * forward_x + delta_y * forward_y
        if depth < BOSS_MIN_FRONT_DEPTH:
            self.x = (camera.x + forward_x * BOSS_RECENTER_DISTANCE) % WORLD_SIZE
            self.y = (camera.y + forward_y * BOSS_RECENTER_DISTANCE) % WORLD_SIZE

        self.heading = self._heading_toward(camera.x, camera.y)
        self.attack_cooldown_remaining = max(0.0, self.attack_cooldown_remaining - dt)

    def fire_if_ready(self, player_x: float, player_y: float) -> list[Projectile]:
        """Vrati burst neprijateljskih projektila ako je hlađenje završeno."""
        if not self.alive or self.attack_cooldown_remaining > 0:
            return []
        heading = self._heading_toward(player_x, player_y)
        self.attack_cooldown_remaining = self.current_cooldown_seconds
        return [
            Projectile(
                x=self.x,
                y=self.y,
                heading=heading + offset,
                speed=self.projectile_speed,
                damage=self.projectile_damage,
                radius=self.projectile_radius,
                lifetime_remaining=self.projectile_lifetime_seconds,
                team="enemy",
                kind="enemy_heavy",
            )
            for offset in self.burst_offsets
        ]
