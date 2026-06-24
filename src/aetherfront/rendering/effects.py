"""Suptilni proceduralni vizualni efekti za borbene povratne informacije."""

import math
from dataclasses import dataclass, field
from enum import StrEnum

import pygame

from aetherfront.config import (
    INTERNAL_SIZE,
    PLAYER_SCREEN_BOTTOM,
    PLAYER_SCREEN_CENTER_X,
)
from aetherfront.rendering.billboards import BillboardProjector, WorldBillboard
from aetherfront.rendering.camera import Camera

EXPLOSION_LIFETIME = 0.34
SPARK_LIFETIME = 0.18
REPAIR_LIFETIME = 0.45
MUZZLE_FLASH_LIFETIME = 0.08
PLAYER_HIT_LIFETIME = 0.16


class EffectKind(StrEnum):
    """Podržane vrste kratkotrajnih vizualnih efekata."""

    EXPLOSION = "explosion"
    BOSS_SPARK = "boss_spark"
    REPAIR = "repair"


@dataclass(slots=True)
class WorldEffect:
    """Efekt vezan uz položaj u omotanom svijetu."""

    kind: EffectKind
    x: float
    y: float
    lifetime: float
    remaining: float
    world_width: float

    @property
    def active(self) -> bool:
        return self.remaining > 0.0

    @property
    def age_ratio(self) -> float:
        return 1.0 - max(0.0, min(1.0, self.remaining / self.lifetime))

    def update(self, dt: float) -> None:
        self.remaining = max(0.0, self.remaining - dt)


@dataclass(slots=True)
class EffectsState:
    """Drži i crta suptilne vizualne efekte bez mijenjanja kamere ili renderera."""

    world_effects: list[WorldEffect] = field(default_factory=list)
    muzzle_flash_remaining: float = 0.0
    player_hit_remaining: float = 0.0

    def add_explosion(self, x: float, y: float) -> None:
        self.world_effects.append(
            WorldEffect(
                kind=EffectKind.EXPLOSION,
                x=x,
                y=y,
                lifetime=EXPLOSION_LIFETIME,
                remaining=EXPLOSION_LIFETIME,
                world_width=46.0,
            )
        )

    def add_boss_spark(self, x: float, y: float) -> None:
        self.world_effects.append(
            WorldEffect(
                kind=EffectKind.BOSS_SPARK,
                x=x,
                y=y,
                lifetime=SPARK_LIFETIME,
                remaining=SPARK_LIFETIME,
                world_width=34.0,
            )
        )

    def add_repair_flash(self, x: float, y: float) -> None:
        self.world_effects.append(
            WorldEffect(
                kind=EffectKind.REPAIR,
                x=x,
                y=y,
                lifetime=REPAIR_LIFETIME,
                remaining=REPAIR_LIFETIME,
                world_width=58.0,
            )
        )

    def trigger_muzzle_flash(self) -> None:
        self.muzzle_flash_remaining = MUZZLE_FLASH_LIFETIME

    def trigger_player_hit(self) -> None:
        self.player_hit_remaining = PLAYER_HIT_LIFETIME

    def update(self, dt: float, *, paused: bool = False) -> None:
        if paused:
            return
        for effect in self.world_effects:
            effect.update(dt)
        self.world_effects = [effect for effect in self.world_effects if effect.active]
        self.muzzle_flash_remaining = max(0.0, self.muzzle_flash_remaining - dt)
        self.player_hit_remaining = max(0.0, self.player_hit_remaining - dt)

    def draw(
        self,
        canvas: pygame.Surface,
        camera: Camera,
        projector: BillboardProjector,
    ) -> None:
        """Nacrtaj svjetske efekte i lokalne efekte igrača prije HUD-a."""
        for effect in self.world_effects:
            surface = create_world_effect_surface(effect)
            projector.draw(
                canvas,
                camera,
                (WorldBillboard(surface, effect.x, effect.y, effect.world_width),),
            )
        if self.muzzle_flash_remaining > 0.0:
            draw_muzzle_flash(canvas, self.muzzle_flash_remaining / MUZZLE_FLASH_LIFETIME)
        if self.player_hit_remaining > 0.0:
            draw_player_hit_marker(canvas, self.player_hit_remaining / PLAYER_HIT_LIFETIME)


def create_world_effect_surface(effect: WorldEffect) -> pygame.Surface:
    """Stvori mali proceduralni sprite za trenutačni frame svjetskog efekta."""
    if effect.kind == EffectKind.EXPLOSION:
        return _create_explosion_surface(effect.age_ratio)
    if effect.kind == EffectKind.REPAIR:
        return _create_repair_flash_surface(effect.age_ratio)
    return _create_boss_spark_surface(effect.age_ratio)


def _create_explosion_surface(age_ratio: float) -> pygame.Surface:
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    alpha = round(210 * (1.0 - age_ratio))
    radius = max(3, round(7 + age_ratio * 11))
    center = (20, 20)
    pygame.draw.circle(surface, (255, 183, 76, alpha), center, radius)
    pygame.draw.circle(surface, (196, 79, 54, alpha), center, max(2, radius - 5), 2)
    for index in range(8):
        angle = index * math.tau / 8
        inner = radius * 0.45
        outer = radius * 1.15
        start = (round(20 + math.cos(angle) * inner), round(20 + math.sin(angle) * inner))
        end = (round(20 + math.cos(angle) * outer), round(20 + math.sin(angle) * outer))
        pygame.draw.line(surface, (236, 190, 83, alpha), start, end, 2)
    return surface


def _create_boss_spark_surface(age_ratio: float) -> pygame.Surface:
    surface = pygame.Surface((34, 34), pygame.SRCALPHA)
    alpha = round(230 * (1.0 - age_ratio))
    radius = max(3, round(5 + age_ratio * 7))
    center = (17, 17)
    pygame.draw.circle(surface, (65, 211, 202, alpha), center, radius, 2)
    pygame.draw.line(surface, (240, 92, 74, alpha), (8, 17), (26, 17), 2)
    pygame.draw.line(surface, (240, 92, 74, alpha), (17, 8), (17, 26), 2)
    return surface


def _create_repair_flash_surface(age_ratio: float) -> pygame.Surface:
    surface = pygame.Surface((48, 48), pygame.SRCALPHA)
    alpha = round(235 * (1.0 - age_ratio))
    radius = max(8, round(12 + age_ratio * 13))
    center = (24, 24)
    pygame.draw.circle(surface, (84, 255, 128, alpha), center, radius, 3)
    pygame.draw.circle(surface, (35, 210, 98, alpha // 2), center, max(5, radius - 6))
    pygame.draw.line(surface, (225, 255, 186, alpha), (24, 10), (24, 38), 5)
    pygame.draw.line(surface, (225, 255, 186, alpha), (10, 24), (38, 24), 5)
    pygame.draw.circle(surface, (232, 255, 205, alpha // 2), center, max(4, radius - 10), 2)
    return surface


def draw_muzzle_flash(canvas: pygame.Surface, intensity: float) -> None:
    """Nacrtaj kratki mjedeni bljesak ispred Kestrela."""
    alpha = round(220 * max(0.0, min(1.0, intensity)))
    x = PLAYER_SCREEN_CENTER_X + 50
    y = PLAYER_SCREEN_BOTTOM - 27
    points = ((x, y), (x + 18, y - 5), (x + 26, y), (x + 18, y + 5))
    pygame.draw.polygon(canvas, (255, 217, 105, alpha), points)
    pygame.draw.circle(canvas, (255, 248, 180, alpha), (x + 8, y), 4)


def draw_player_hit_marker(canvas: pygame.Surface, intensity: float) -> None:
    """Nacrtaj lokalni crveni damage marker bez zasljepljujućeg full-screen flasha."""
    alpha = round(105 * max(0.0, min(1.0, intensity)))
    marker = pygame.Surface(INTERNAL_SIZE, pygame.SRCALPHA)
    pygame.draw.rect(marker, (193, 63, 57, alpha), (0, INTERNAL_SIZE[1] - 30, INTERNAL_SIZE[0], 30))
    pygame.draw.rect(marker, (193, 63, 57, alpha // 2), (0, 0, INTERNAL_SIZE[0], 8))
    canvas.blit(marker, (0, 0))
