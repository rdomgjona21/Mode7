"""Model popravka koji liječi igrača i dodaje bodove."""

import math
from dataclasses import dataclass

from aetherfront.gameplay.collisions import CircleBody
from aetherfront.gameplay.player import PlayerCombatState


@dataclass(slots=True)
class RepairPickup:
    """Privremeni pickup na položaju uništenog cilja."""

    x: float
    y: float
    heal_amount: float
    score_value: int
    radius: float
    lifetime_remaining: float

    @property
    def active(self) -> bool:
        """Pickup postoji dok nije prikupljen ili istekao."""
        return self.lifetime_remaining > 0

    @property
    def collision_body(self) -> CircleBody:
        """Vrati kružni oblik za provjeru s igračem."""
        return CircleBody(self.x, self.y, self.radius)

    def update(self, dt: float) -> bool:
        """Smanji trajanje i vrati ostaje li pickup aktivan."""
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("delta time must be finite and non-negative")
        self.lifetime_remaining = max(0.0, self.lifetime_remaining - dt)
        return self.active

    def collect(self, player: PlayerCombatState) -> tuple[float, int]:
        """Primijeni popravak jednom i vrati obnovljeno zdravlje i bodove."""
        if not self.active:
            return 0.0, 0
        healed = player.heal(self.heal_amount)
        self.lifetime_remaining = 0.0
        return healed, self.score_value
