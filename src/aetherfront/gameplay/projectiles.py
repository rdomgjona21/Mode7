"""Model projektila s vremenski neovisnim kretanjem i ograničenim trajanjem."""

import math
from dataclasses import dataclass

from aetherfront.config import WORLD_SIZE
from aetherfront.gameplay.collisions import CircleBody


@dataclass(slots=True)
class Projectile:
    """Jedan projektil u koordinatama omotanog svijeta."""

    x: float
    y: float
    heading: float
    speed: float
    damage: float
    radius: float
    lifetime_remaining: float
    team: str

    def __post_init__(self) -> None:
        """Provjeri vrijednosti potrebne za stabilnu simulaciju."""
        numeric_values = (self.x, self.y, self.heading, self.speed, self.damage)
        if not all(math.isfinite(value) for value in numeric_values):
            raise ValueError("projectile values must be finite")
        if self.speed < 0 or self.damage < 0:
            raise ValueError("projectile speed and damage must be non-negative")
        if not math.isfinite(self.radius) or self.radius <= 0:
            raise ValueError("projectile radius must be positive and finite")
        if not math.isfinite(self.lifetime_remaining) or self.lifetime_remaining <= 0:
            raise ValueError("projectile lifetime must be positive and finite")
        if not self.team:
            raise ValueError("projectile team must not be empty")
        self.heading %= math.tau

    @property
    def active(self) -> bool:
        """Projektil postoji dok mu nije isteklo trajanje."""
        return self.lifetime_remaining > 0

    @property
    def collision_body(self) -> CircleBody:
        """Vrati trenutni kružni oblik za provjeru sudara."""
        return CircleBody(self.x, self.y, self.radius)

    def update(self, dt: float, world_size: float = WORLD_SIZE) -> bool:
        """Pomakni projektil, smanji trajanje i vrati ostaje li aktivan."""
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("delta time must be finite and non-negative")
        if not math.isfinite(world_size) or world_size <= 0:
            raise ValueError("world size must be positive and finite")
        if not self.active:
            return False

        self.x = (self.x + math.cos(self.heading) * self.speed * dt) % world_size
        self.y = (self.y + math.sin(self.heading) * self.speed * dt) % world_size
        self.lifetime_remaining = max(0.0, self.lifetime_remaining - dt)
        return self.active
