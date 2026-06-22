"""Projekcija i crtanje 2D objekata postavljenih u omotani Mode7 svijet."""

import math
from collections.abc import Iterable
from dataclasses import dataclass

import pygame

from aetherfront.config import (
    CAMERA_HEIGHT,
    HORIZON_Y,
    HORIZONTAL_FOV_DEGREES,
    INTERNAL_SIZE,
    MAX_VIEW_DISTANCE,
    WORLD_SIZE,
)
from aetherfront.rendering.camera import Camera


@dataclass(frozen=True, slots=True)
class WorldBillboard:
    """2D slika s položajem i širinom izraženima u koordinatama svijeta."""

    surface: pygame.Surface
    x: float
    y: float
    world_width: float

    def __post_init__(self) -> None:
        """Odbij objekte koji se ne mogu smisleno projicirati."""
        if self.surface.get_width() < 1 or self.surface.get_height() < 1:
            raise ValueError("billboard surface dimensions must be positive")
        if not math.isfinite(self.x) or not math.isfinite(self.y):
            raise ValueError("billboard position must be finite")
        if not math.isfinite(self.world_width) or self.world_width <= 0:
            raise ValueError("billboard world width must be positive and finite")


@dataclass(frozen=True, slots=True)
class ProjectedBillboard:
    """Rezultat projekcije spreman za skaliranje i crtanje na zaslon."""

    source: WorldBillboard
    rect: pygame.Rect
    depth: float


class BillboardProjector:
    """Pretvara položaje svijeta u perspektivne pravokutnike na zaslonu."""

    def __init__(
        self,
        width: int = INTERNAL_SIZE[0],
        height: int = INTERNAL_SIZE[1],
        horizon: int = HORIZON_Y,
        horizontal_fov_degrees: float = HORIZONTAL_FOV_DEGREES,
        camera_height: float = CAMERA_HEIGHT,
        world_size: float = WORLD_SIZE,
        near_clip: float = 1.0,
        far_clip: float = MAX_VIEW_DISTANCE,
    ) -> None:
        """Spremi projekcijske postavke i izračunaj žarišnu duljinu."""
        if width < 2 or height < 2:
            raise ValueError("projection dimensions must be at least 2")
        if not 0 <= horizon < height:
            raise ValueError("horizon must be inside the display")
        if not 0 < horizontal_fov_degrees < 180:
            raise ValueError("horizontal FOV must be between 0 and 180 degrees")
        if camera_height <= 0 or world_size <= 0:
            raise ValueError("camera height and world size must be positive")
        if near_clip <= 0 or far_clip <= near_clip:
            raise ValueError("clipping distances must be positive and ordered")

        self.width = width
        self.height = height
        self.horizon = horizon
        self.camera_height = camera_height
        self.world_size = world_size
        self.near_clip = near_clip
        self.far_clip = far_clip
        half_fov_tangent = math.tan(math.radians(horizontal_fov_degrees) / 2)
        self.focal_length = (width / 2) / half_fov_tangent

    def _wrapped_delta(self, target: float, origin: float) -> float:
        """Vrati najkraći potpisani pomak kroz omotanu os svijeta."""
        return (target - origin + self.world_size / 2) % self.world_size - self.world_size / 2

    def project(
        self, camera: Camera, billboard: WorldBillboard
    ) -> ProjectedBillboard | None:
        """Projiciraj jedan objekt ili vrati ``None`` ako nije vidljiv."""
        delta_x = self._wrapped_delta(billboard.x, camera.x)
        delta_y = self._wrapped_delta(billboard.y, camera.y)

        forward_x = math.cos(camera.heading)
        forward_y = math.sin(camera.heading)
        depth = delta_x * forward_x + delta_y * forward_y
        if depth <= self.near_clip or depth > self.far_clip:
            return None

        lateral = delta_x * -forward_y + delta_y * forward_x
        screen_x = self.width / 2 + lateral * self.focal_length / depth
        ground_y = self.horizon + self.camera_height * self.focal_length / depth

        pixel_width = max(1, round(billboard.world_width * self.focal_length / depth))
        aspect_ratio = billboard.surface.get_height() / billboard.surface.get_width()
        pixel_height = max(1, round(pixel_width * aspect_ratio))
        rect = pygame.Rect(0, 0, pixel_width, pixel_height)
        rect.midbottom = (round(screen_x), round(ground_y))

        outside_display = (
            rect.right <= 0
            or rect.left >= self.width
            or rect.bottom <= 0
            or rect.top >= self.height
        )
        if outside_display:
            return None
        return ProjectedBillboard(source=billboard, rect=rect, depth=depth)

    def project_all(
        self, camera: Camera, billboards: Iterable[WorldBillboard]
    ) -> list[ProjectedBillboard]:
        """Projiciraj vidljive objekte i poredaj ih od najudaljenijeg prema najbližem."""
        projected = [
            result
            for billboard in billboards
            if (result := self.project(camera, billboard)) is not None
        ]
        return sorted(projected, key=lambda item: item.depth, reverse=True)

    def draw(
        self,
        canvas: pygame.Surface,
        camera: Camera,
        billboards: Iterable[WorldBillboard],
    ) -> int:
        """Skaliraj i nacrtaj sve vidljive objekte te vrati njihov broj."""
        if canvas.get_size() != (self.width, self.height):
            raise ValueError("canvas dimensions must match billboard projection")

        projected = self.project_all(camera, billboards)
        for item in projected:
            scaled = pygame.transform.smoothscale(item.source.surface, item.rect.size)
            canvas.blit(scaled, item.rect)
        return len(projected)
