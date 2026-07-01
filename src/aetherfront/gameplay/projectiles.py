"""Model projektila s vremenski neovisnim kretanjem i ograničenim trajanjem."""

import math
from dataclasses import dataclass

from aetherfront.config import WORLD_SIZE
from aetherfront.gameplay.collisions import CircleBody
from aetherfront.gameplay.validation import (
    require_all_finite,
    require_non_negative,
    require_positive,
    require_text,
)


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
    kind: str = "cannon"

    def __post_init__(self) -> None:
        """Provjeri vrijednosti potrebne za stabilnu simulaciju."""
        require_all_finite(
            (
                ("projectile x", self.x),
                ("projectile y", self.y),
                ("projectile heading", self.heading),
            )
        )
        require_non_negative(self.speed, "projectile speed")
        require_non_negative(self.damage, "projectile damage")
        require_positive(self.radius, "projectile radius")
        require_positive(self.lifetime_remaining, "projectile lifetime")
        require_text(self.team, "projectile team")
        require_text(self.kind, "projectile kind")
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
