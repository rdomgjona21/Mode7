"""Povezuje oružja, protivnike, projektile, pickup, zdravlje i bodove."""

import math
from dataclasses import dataclass, field

from aetherfront.config import WORLD_SIZE
from aetherfront.gameplay.balance import CombatBalance, load_combat_balance
from aetherfront.gameplay.boss import DreadnoughtBoss
from aetherfront.gameplay.collisions import CircleBody, circles_overlap, wrapped_axis_delta
from aetherfront.gameplay.enemies import Enemy
from aetherfront.gameplay.pickups import RepairPickup
from aetherfront.gameplay.player import PlayerCombatState
from aetherfront.gameplay.projectiles import Projectile
from aetherfront.gameplay.waves import WaveDirector
from aetherfront.gameplay.weapons import PrimaryWeapon, WeaponController
from aetherfront.rendering.camera import Camera

MIN_VISIBLE_ENEMY_DEPTH = 150.0
RECYCLED_ENEMY_DEPTH = 650.0
RECYCLED_ENEMY_SIDE_STEP = 115.0
RECYCLED_ENEMY_COOLDOWN_SECONDS = 0.8


@dataclass(slots=True)
class CombatSession:
    """Trenutačno borbeno stanje koje glavna petlja ažurira jednom po frameu."""

    balance: CombatBalance
    player: PlayerCombatState
    weapons: WeaponController
    wave_director: WaveDirector
    enemies: list[Enemy]
    boss: DreadnoughtBoss | None = None
    projectiles: list[Projectile] = field(default_factory=list)
    pickups: list[RepairPickup] = field(default_factory=list)
    score: int = 0

    @classmethod
    def create(cls, camera: Camera) -> "CombatSession":
        """Učitaj balans i postavi prvi konfigurirani val standardnih protivnika."""
        balance = load_combat_balance()
        wave_director = WaveDirector.create()
        enemies = wave_director.update(0.0, camera, balance, living_enemy_count=0)
        return cls(
            balance=balance,
            player=PlayerCombatState.from_balance(balance.player),
            weapons=WeaponController.from_balance(balance),
            wave_director=wave_director,
            enemies=enemies,
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

    def _hit_boss(self) -> None:
        """Primijeni pogotke igrača na aktivnog bossa bez zatvaranja borbe."""
        if self.boss is None or not self.boss.alive:
            return
        for projectile in self.projectiles:
            if projectile.team != "player":
                continue
            if circles_overlap(projectile.collision_body, self.boss.collision_body):
                projectile.lifetime_remaining = 0.0
                self.boss.take_damage(projectile.damage)
        self.projectiles = [projectile for projectile in self.projectiles if projectile.active]

    def _update_enemies(self, dt: float, camera: Camera) -> None:
        for enemy in self.enemies:
            enemy.update(dt, camera.x, camera.y)
            if self._available_projectile_slots() <= 0:
                continue
            projectile = enemy.fire_if_ready(camera.x, camera.y)
            if projectile is not None:
                self.projectiles.append(projectile)

    def _update_boss(self, dt: float, camera: Camera) -> None:
        """Ažuriraj boss položaj i dodaj njegov burst ako je hlađenje spremno."""
        if self.boss is None or not self.boss.alive:
            return
        self.boss.update(dt, camera)
        available_slots = self._available_projectile_slots()
        if available_slots <= 0:
            return
        self.projectiles.extend(self.boss.fire_if_ready(camera.x, camera.y)[:available_slots])

    def _ensure_boss_spawned(self, camera: Camera) -> None:
        """Stvori ISS Goliath nakon završetka trećeg vala."""
        if not self.wave_director.waves_complete or self.boss is not None:
            return
        self.boss = DreadnoughtBoss.spawn_ahead(camera, self.balance.boss)

    def _keep_enemies_in_front(self, camera: Camera) -> None:
        """Vrati prebliske ili iza-kamere protivnike u vidljivi prednji sektor."""
        forward_x = math.cos(camera.heading)
        forward_y = math.sin(camera.heading)
        right_x = -math.sin(camera.heading)
        right_y = math.cos(camera.heading)
        for index, enemy in enumerate(self.enemies):
            delta_x = wrapped_axis_delta(camera.x, enemy.x)
            delta_y = wrapped_axis_delta(camera.y, enemy.y)
            depth = delta_x * forward_x + delta_y * forward_y
            if depth >= MIN_VISIBLE_ENEMY_DEPTH:
                continue

            side = ((index % 5) - 2) * RECYCLED_ENEMY_SIDE_STEP
            enemy.x = (camera.x + forward_x * RECYCLED_ENEMY_DEPTH + right_x * side) % WORLD_SIZE
            enemy.y = (camera.y + forward_y * RECYCLED_ENEMY_DEPTH + right_y * side) % WORLD_SIZE
            enemy.heading = (camera.heading + math.pi) % math.tau
            enemy.attack_cooldown_remaining = max(
                enemy.attack_cooldown_remaining,
                RECYCLED_ENEMY_COOLDOWN_SECONDS,
            )

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
        if self.boss is not None and self.boss.alive:
            if circles_overlap(player_body, self.boss.collision_body):
                self.player.take_damage(self.boss.contact_damage)
        self.projectiles = [projectile for projectile in self.projectiles if projectile.active]

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
        self.enemies.extend(
            self.wave_director.update(
                dt,
                camera,
                self.balance,
                living_enemy_count=self.enemies_remaining,
            )
        )
        self._ensure_boss_spawned(camera)
        self._fire(camera, fire_primary, fire_rocket)
        self._update_enemies(dt, camera)
        self._keep_enemies_in_front(camera)
        self._update_boss(dt, camera)
        self._update_projectiles(dt)
        self._hit_enemies()
        self._hit_boss()
        self._hit_player(camera)
        self.enemies.extend(
            self.wave_director.update(
                0.0,
                camera,
                self.balance,
                living_enemy_count=self.enemies_remaining,
            )
        )
        self._ensure_boss_spawned(camera)
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
