"""Privremeni trening-cilj za ručnu provjeru oružja prije neprijatelja."""

import math
from dataclasses import dataclass, field

from aetherfront.config import WORLD_SIZE
from aetherfront.gameplay.collisions import CircleBody
from aetherfront.rendering.camera import Camera

TRAINING_TARGET_HEALTH = 100.0
TRAINING_TARGET_RADIUS = 18.0
TRAINING_TARGET_DISTANCE = 400.0
TRAINING_TARGET_RESPAWN_SECONDS = 1.5


@dataclass(slots=True)
class TrainingTarget:
    """Statičan cilj koji prima štetu i može se ponovno postaviti."""

    x: float
    y: float
    max_health: float = TRAINING_TARGET_HEALTH
    radius: float = TRAINING_TARGET_RADIUS
    health: float = field(init=False)

    def __post_init__(self) -> None:
        self.health = self.max_health

    @classmethod
    def ahead_of(cls, camera: Camera) -> "TrainingTarget":
        """Postavi cilj ispred trenutačnog smjera igrača."""
        return cls(
            x=(camera.x + math.cos(camera.heading) * TRAINING_TARGET_DISTANCE) % WORLD_SIZE,
            y=(camera.y + math.sin(camera.heading) * TRAINING_TARGET_DISTANCE) % WORLD_SIZE,
        )

    @property
    def alive(self) -> bool:
        return self.health > 0

    @property
    def collision_body(self) -> CircleBody:
        return CircleBody(self.x, self.y, self.radius)

    def take_damage(self, amount: float) -> bool:
        """Primijeni štetu i vrati je li ovaj pogodak uništio cilj."""
        if not math.isfinite(amount) or amount < 0:
            raise ValueError("damage must be finite and non-negative")
        if not self.alive or amount == 0:
            return False
        self.health = max(0.0, self.health - amount)
        return not self.alive
