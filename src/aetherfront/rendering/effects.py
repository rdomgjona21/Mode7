"""Flash overlay i čestice eksplozija kao vizualna povratna informacija."""

import math
import random
from dataclasses import dataclass, field

import pygame

from aetherfront.config import INTERNAL_SIZE
from aetherfront.rendering.billboards import BillboardProjector, WorldBillboard


@dataclass(slots=True)
class ExplosionParticle:
    """Jedna čestica eksplozije s pozicijom u svjetskim koordinatama."""

    x: float
    y: float
    vx: float
    vy: float
    size: float
    lifetime: float
    lifetime_remaining: float

    @property
    def active(self) -> bool:
        return self.lifetime_remaining > 0.0

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime_remaining -= dt


def spawn_explosion(x: float, y: float, count: int = 10) -> list[ExplosionParticle]:
    """Stvori čestice eksplozije na zadanoj svjetskoj poziciji."""
    particles = []
    for _ in range(count):
        angle = random.uniform(0.0, math.tau)
        speed = random.uniform(40.0, 140.0)
        lifetime = random.uniform(0.25, 0.55)
        particles.append(
            ExplosionParticle(
                x=x,
                y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                size=random.uniform(2.0, 5.0),
                lifetime=lifetime,
                lifetime_remaining=lifetime,
            )
        )
    return particles


def update_particles(particles: list[ExplosionParticle], dt: float) -> list[ExplosionParticle]:
    for p in particles:
        p.update(dt)
    return [p for p in particles if p.active]


def draw_particles(
    canvas: pygame.Surface,
    camera_x: float,
    camera_y: float,
    projector: BillboardProjector,
    particles: list[ExplosionParticle],
) -> None:
    """Projiciraj čestice kao billboarde i nacrtaj ih kao obojene krugove."""
    if not particles:
        return
    billboards = [
        WorldBillboard(surface=None, world_x=p.x, world_y=p.y, world_diameter=p.size * 2)  # type: ignore[arg-type]
        for p in particles
    ]
    projected = projector.project_all(
        type("_Cam", (), {"x": camera_x, "y": camera_y, "heading": 0.0})(),  # type: ignore[arg-type]
        billboards,
    )
    for proj, particle in zip(projected, particles, strict=False):
        if proj is None:
            continue
        alpha_ratio = particle.lifetime_remaining / particle.lifetime
        color = (255, int(180 * alpha_ratio), int(40 * alpha_ratio))
        radius = max(1, int(proj.screen_rect.width / 2))
        pygame.draw.circle(canvas, color, proj.screen_rect.center, radius)


@dataclass(slots=True)
class EffectsState:
    """Drži trenutačno stanje flash overlaya i aktivnih čestica."""

    flash_alpha: float = 0.0
    flash_remaining: float = 0.0
    particles: list[ExplosionParticle] = field(default_factory=list)

    def trigger_flash(self, alpha: float, duration: float) -> None:
        self.flash_alpha = max(self.flash_alpha, alpha)
        self.flash_remaining = max(self.flash_remaining, duration)

    def add_explosion(self, x: float, y: float) -> None:
        self.particles.extend(spawn_explosion(x, y))

    def update(self, dt: float) -> None:
        if self.flash_remaining > 0.0:
            self.flash_remaining -= dt
            if self.flash_remaining <= 0.0:
                self.flash_alpha = 0.0
                self.flash_remaining = 0.0
        self.particles = update_particles(self.particles, dt)

    def draw(
        self,
        canvas: pygame.Surface,
        camera_x: float,
        camera_y: float,
        projector: BillboardProjector,
    ) -> None:
        draw_particles(canvas, camera_x, camera_y, projector, self.particles)
        if self.flash_alpha > 0.0:
            overlay = pygame.Surface(INTERNAL_SIZE, pygame.SRCALPHA)
            overlay.fill((255, 255, 255, int(self.flash_alpha)))
            canvas.blit(overlay, (0, 0))
