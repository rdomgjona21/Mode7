"""Borbeno stanje igrača odvojeno od kretanja kamere i crtanja broda."""

import math
from dataclasses import dataclass, field

from aetherfront.gameplay.balance import PlayerBalance


@dataclass(slots=True)
class PlayerCombatState:
    """Čuva zdravlje i preostalo vrijeme neranjivosti igrača."""

    max_health: float
    invulnerability_duration: float
    health: float = field(init=False)
    invulnerability_remaining: float = field(default=0.0, init=False)

    def __post_init__(self) -> None:
        """Pokreni igrača s punim zdravljem nakon provjere postavki."""
        if not math.isfinite(self.max_health) or self.max_health <= 0:
            raise ValueError("maximum health must be positive and finite")
        if (
            not math.isfinite(self.invulnerability_duration)
            or self.invulnerability_duration <= 0
        ):
            raise ValueError("invulnerability duration must be positive and finite")
        self.health = self.max_health

    @classmethod
    def from_balance(cls, balance: PlayerBalance) -> "PlayerCombatState":
        """Stvori stanje iz provjerene JSON konfiguracije."""
        return cls(
            max_health=balance.max_health,
            invulnerability_duration=balance.invulnerability_seconds,
        )

    @property
    def alive(self) -> bool:
        """Igrač je živ dok ima barem malo zdravlja."""
        return self.health > 0

    @property
    def invulnerable(self) -> bool:
        """Vrati je li aktivna zaštita nakon zadnjeg pogotka."""
        return self.invulnerability_remaining > 0

    def update(self, dt: float) -> None:
        """Smanji preostalo vrijeme neranjivosti bez prelaska ispod nule."""
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("delta time must be finite and non-negative")
        self.invulnerability_remaining = max(0.0, self.invulnerability_remaining - dt)

    def take_damage(self, amount: float) -> bool:
        """Primijeni štetu ako je dopuštena i javi je li pogodak prihvaćen."""
        if not math.isfinite(amount) or amount < 0:
            raise ValueError("damage must be finite and non-negative")
        if amount == 0 or not self.alive or self.invulnerable:
            return False

        self.health = max(0.0, self.health - amount)
        self.invulnerability_remaining = self.invulnerability_duration
        return True

    def heal(self, amount: float) -> float:
        """Vrati zdravlje do maksimuma i javi koliko je stvarno obnovljeno."""
        if not math.isfinite(amount) or amount < 0:
            raise ValueError("healing must be finite and non-negative")
        previous = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - previous
