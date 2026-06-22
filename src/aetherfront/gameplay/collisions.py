"""Deterministički kružni sudari u svijetu koji se omata po obje osi."""

import math
from dataclasses import dataclass

from aetherfront.config import WORLD_SIZE


@dataclass(frozen=True, slots=True)
class CircleBody:
    """Kružni oblik sudara izražen koordinatama svijeta."""

    x: float
    y: float
    radius: float

    def __post_init__(self) -> None:
        """Odbij neupotrebljiv položaj ili radijus."""
        if not math.isfinite(self.x) or not math.isfinite(self.y):
            raise ValueError("circle position must be finite")
        if not math.isfinite(self.radius) or self.radius <= 0:
            raise ValueError("circle radius must be positive and finite")


def wrapped_axis_delta(first: float, second: float, world_size: float = WORLD_SIZE) -> float:
    """Vrati najkraći potpisani pomak od prve do druge točke na jednoj osi."""
    if not math.isfinite(world_size) or world_size <= 0:
        raise ValueError("world size must be positive and finite")
    return (second - first + world_size / 2) % world_size - world_size / 2


def circles_overlap(
    first: CircleBody,
    second: CircleBody,
    world_size: float = WORLD_SIZE,
) -> bool:
    """Provjeri dodiruju li se kružnice najkraćim putem kroz omotani svijet."""
    delta_x = wrapped_axis_delta(first.x, second.x, world_size)
    delta_y = wrapped_axis_delta(first.y, second.y, world_size)
    combined_radius = first.radius + second.radius
    return delta_x * delta_x + delta_y * delta_y <= combined_radius * combined_radius
