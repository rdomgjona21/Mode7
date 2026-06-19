"""Položaj i kretanje kamere kroz omotani svijet."""

import math
from dataclasses import dataclass

from aetherfront.config import (
    MAX_SPEED,
    MIN_SPEED,
    SPEED_CHANGE_RATE,
    TURN_RATE,
    WORLD_SIZE,
)


def _clamp(value: float, minimum: float, maximum: float) -> float:
    """Ograniči vrijednost na zatvoreni interval minimum-maksimum."""
    return max(minimum, min(value, maximum))


@dataclass(slots=True)
class Camera:
    """Opisuje položaj, smjer i brzinu promatrača u svijetu igre."""

    x: float = WORLD_SIZE / 2
    y: float = WORLD_SIZE / 2
    heading: float = 0.0
    speed: float = MIN_SPEED

    def update(self, dt: float, turn: float = 0.0, throttle: float = 0.0) -> None:
        """Ažuriraj kameru za proteklo vrijeme i normalizirane ulaze od -1 do 1."""
        if dt < 0:
            raise ValueError("dt must not be negative")

        turn = _clamp(turn, -1.0, 1.0)
        throttle = _clamp(throttle, -1.0, 1.0)

        # Smjer se čuva u radijanima unutar jednog punog kruga.
        self.heading = (self.heading + turn * TURN_RATE * dt) % math.tau
        self.speed = _clamp(
            self.speed + throttle * SPEED_CHANGE_RATE * dt,
            MIN_SPEED,
            MAX_SPEED,
        )

        # Kosinus daje pomak po osi x, a sinus pomak po osi y.
        self.x = (self.x + math.cos(self.heading) * self.speed * dt) % WORLD_SIZE
        self.y = (self.y + math.sin(self.heading) * self.speed * dt) % WORLD_SIZE
