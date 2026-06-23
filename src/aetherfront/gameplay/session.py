"""Povezuje oružja, protivnike, projektile, pickup, zdravlje i bodove."""

import math
from dataclasses import dataclass, field

from aetherfront.config import WORLD_SIZE
from aetherfront.gameplay.balance import CombatBalance, load_combat_balance
from aetherfront.gameplay.collisions import CircleBody, circles_overlap
from aetherfront.gameplay.enemies import Enemy, EnemyKind
from aetherfront.gameplay.pickups import RepairPickup
from aetherfront.gameplay.player import PlayerCombatState
from aetherfront.gameplay.projectiles import Projectile
from aetherfront.gameplay.weapons import PrimaryWeapon, WeaponController
from aetherfront.rendering.camera import Camera

ENEMY_GROUP_RESPAWN_SECONDS = 2.0


@dataclass(slots=True)
class CombatSession:
    """Trenutačno borbeno stanje koje glavna petlja ažurira jednom po frameu."""

    balance: CombatBalance
    player: PlayerCombatState
    weapons: WeaponController
    enemies: list[Enemy]
    projectiles: list[Projectile] = field(default_factory=list)
    pickups: list[RepairPickup] = field(default_factory=list)
    score: int = 0
    enemy_group_respawn_remaining: float = 0.0

    @classmethod
    def create(cls, camera: Camera) -> "CombatSession":
        """Učitaj balans i postavi prvu testnu skupinu standardnih protivnika."""
        balance = load_combat_balance()
        return cls(
            balance=balance,
            player=PlayerCombatState.from_balance(balance.player),
            weapons=WeaponController.from_balance(balance),
            enemies=_spawn_enemy_group(balance, camera),
        )

    def select_primary(self, weapon: PrimaryWeapon) -> None:
        """Proslijedi odabir primarnog oružja kontroleru."""
        self.weapons.select_primary(weapon)

    def _available_projectile_slots(self) -> int:
        return max(0, self.balance.projectile.limit - len(self.projectiles))

    def _fire(self, camera: Camera, fire_primary: bool, fire_rocket: bool) -> None:
        """Dodaj projektile koje su ulazi i hlađenja dopustili u ovom frameu."""
        if fire_primary:
            self.projectiles.extend(
                self.weapons.fire_primary(
                    camera.x,
                    camera.y,
                    camera.heading,
                    self._available_projectile_slots(),
                )
            )
        if fire_rocket:
            self.projectiles.extend(
                self.weapons.fire_rocket(
                    camera.x,
                    camera.y,
                    camera.heading,
                    self._available_projectile_slots(),
                )
            )

    def _update_projectiles(self, dt: float) -> None:
        for projectile in self.projectiles:
            projectile.update(dt)
        self.projectiles = [projectile for projectile in self.projectiles if projectile.active]

    def _create_repair(self, x: float, y: float) -> None:
        repair = self.balance.repair
        self.pickups.append(
            RepairPickup(
                x=x,
                y=y,
                heal_amount=repair.heal_amount,
                score_value=repair.score_value,
                radius=repair.collision_radius,
                lifetime_remaining=repair.lifetime_seconds,
            )
        )

    def _hit_enemies(self) -> None:
        """Primijeni prvi sudar svakog igračeva projektila s aktivnim protivnikom."""
        for projectile in self.projectiles:
            if projectile.team != "player":
                continue
            for enemy in self.enemies:
                if not enemy.alive:
                    continue
                if circles_overlap(projectile.collision_body, enemy.collision_body):
                    projectile.lifetime_remaining = 0.0
                    destroyed = enemy.take_damage(projectile.damage)
                    if destroyed:
                        self.score += enemy.score_value
                        self._create_repair(enemy.x, enemy.y)
                    break
        self.projectiles = [projectile for projectile in self.projectiles if projectile.active]
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        if not self.enemies and self.enemy_group_respawn_remaining <= 0:
            self.enemy_group_respawn_remaining = ENEMY_GROUP_RESPAWN_SECONDS

    def _update_enemies(self, dt: float, camera: Camera) -> None:
        for enemy in self.enemies:
            enemy.update(dt, camera.x, camera.y)
            if self._available_projectile_slots() <= 0:
                continue
            projectile = enemy.fire_if_ready(camera.x, camera.y)
            if projectile is not None:
                self.projectiles.append(projectile)

    def _hit_player(self, camera: Camera) -> None:
        player_body = CircleBody(camera.x, camera.y, self.balance.player.collision_radius)
        for projectile in self.projectiles:
            if projectile.team != "enemy":
                continue
            if circles_overlap(player_body, projectile.collision_body):
                self.player.take_damage(projectile.damage)
                projectile.lifetime_remaining = 0.0
        for enemy in self.enemies:
            if circles_overlap(player_body, enemy.collision_body):
                self.player.take_damage(enemy.contact_damage)
        self.projectiles = [projectile for projectile in self.projectiles if projectile.active]

    def _update_enemy_respawn(self, dt: float, camera: Camera) -> None:
        if self.enemies:
            return
        self.enemy_group_respawn_remaining = max(0.0, self.enemy_group_respawn_remaining - dt)
        if self.enemy_group_respawn_remaining <= 0:
            self.enemies = _spawn_enemy_group(self.balance, camera)

    def _update_pickups(self, dt: float, camera: Camera) -> None:
        player_body = CircleBody(camera.x, camera.y, self.balance.player.collision_radius)
        for pickup in self.pickups:
            pickup.update(dt)
            if pickup.active and circles_overlap(player_body, pickup.collision_body):
                _, awarded_score = pickup.collect(self.player)
                self.score += awarded_score
        self.pickups = [pickup for pickup in self.pickups if pickup.active]

    def update(
        self,
        dt: float,
        camera: Camera,
        fire_primary: bool = False,
        fire_rocket: bool = False,
    ) -> None:
        """Ažuriraj trenutni testni sukob protiv standardnih protivnika."""
        self.player.update(dt)
        self.weapons.update(dt)
        self._fire(camera, fire_primary, fire_rocket)
        self._update_enemies(dt, camera)
        self._update_projectiles(dt)
        self._hit_enemies()
        self._hit_player(camera)
        self._update_enemy_respawn(dt, camera)
        self._update_pickups(dt, camera)

    @property
    def enemies_remaining(self) -> int:
        """Broj živih standardnih protivnika u trenutačnoj probnoj skupini."""
        return sum(1 for enemy in self.enemies if enemy.alive)

    @property
    def lowest_health_enemy(self) -> Enemy | None:
        """Vrati živog protivnika s najmanje preostalog trupa za kratki HUD prikaz."""
        living = [enemy for enemy in self.enemies if enemy.alive]
        if not living:
            return None
        return min(living, key=lambda enemy: enemy.health or 0.0)


def _spawn_enemy_group(balance: CombatBalance, camera: Camera) -> list[Enemy]:
    """Postavi malu razvojnu skupinu s jednom ili više svake zaključane vrste."""
    forward_x = math.cos(camera.heading)
    forward_y = math.sin(camera.heading)
    right_x = -math.sin(camera.heading)
    right_y = math.cos(camera.heading)
    placements = (
        (EnemyKind.SCOUT, 390.0, -135.0, 0.25),
        (EnemyKind.SCOUT, 470.0, 125.0, 0.85),
        (EnemyKind.GUNSHIP, 560.0, -25.0, 0.45),
        (EnemyKind.BOMBER, 710.0, 165.0, 1.15),
    )
    enemies: list[Enemy] = []
    for kind, forward, side, cooldown_factor in placements:
        x = (camera.x + forward_x * forward + right_x * side) % WORLD_SIZE
        y = (camera.y + forward_y * forward + right_y * side) % WORLD_SIZE
        enemy_balance = balance.enemies[kind.value]
        enemies.append(
            Enemy.from_balance(
                kind,
                enemy_balance,
                x,
                y,
                heading=(camera.heading + math.pi) % math.tau,
                attack_cooldown_remaining=enemy_balance.attack_cooldown_seconds
                * cooldown_factor,
            )
        )
    return enemies
