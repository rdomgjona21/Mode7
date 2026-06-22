"""Povezuje oružja, projektile, cilj, pickup, zdravlje i bodove u igrivu probu."""

from dataclasses import dataclass, field

from aetherfront.gameplay.balance import CombatBalance, load_combat_balance
from aetherfront.gameplay.collisions import CircleBody, circles_overlap
from aetherfront.gameplay.pickups import RepairPickup
from aetherfront.gameplay.player import PlayerCombatState
from aetherfront.gameplay.projectiles import Projectile
from aetherfront.gameplay.targets import TRAINING_TARGET_RESPAWN_SECONDS, TrainingTarget
from aetherfront.gameplay.weapons import PrimaryWeapon, WeaponController
from aetherfront.rendering.camera import Camera


@dataclass(slots=True)
class CombatSession:
    """Trenutačno borbeno stanje koje glavna petlja ažurira jednom po frameu."""

    balance: CombatBalance
    player: PlayerCombatState
    weapons: WeaponController
    target: TrainingTarget
    projectiles: list[Projectile] = field(default_factory=list)
    pickups: list[RepairPickup] = field(default_factory=list)
    score: int = 0
    target_respawn_remaining: float = 0.0

    @classmethod
    def create(cls, camera: Camera) -> "CombatSession":
        """Učitaj balans i postavi početni trening-cilj ispred igrača."""
        balance = load_combat_balance()
        return cls(
            balance=balance,
            player=PlayerCombatState.from_balance(balance.player),
            weapons=WeaponController.from_balance(balance),
            target=TrainingTarget.ahead_of(camera),
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

    def _hit_target(self) -> None:
        """Primijeni prvi sudar svakog projektila i stvori popravak nakon uništenja."""
        if not self.target.alive:
            return
        for projectile in self.projectiles:
            if projectile.team != "player":
                continue
            if circles_overlap(projectile.collision_body, self.target.collision_body):
                projectile.lifetime_remaining = 0.0
                destroyed = self.target.take_damage(projectile.damage)
                if destroyed:
                    repair = self.balance.repair
                    self.pickups.append(
                        RepairPickup(
                            x=self.target.x,
                            y=self.target.y,
                            heal_amount=repair.heal_amount,
                            score_value=repair.score_value,
                            radius=repair.collision_radius,
                            lifetime_remaining=repair.lifetime_seconds,
                        )
                    )
                    self.target_respawn_remaining = TRAINING_TARGET_RESPAWN_SECONDS
                    break
        self.projectiles = [projectile for projectile in self.projectiles if projectile.active]

    def _update_target_respawn(self, dt: float, camera: Camera) -> None:
        if self.target.alive:
            return
        self.target_respawn_remaining = max(0.0, self.target_respawn_remaining - dt)
        if self.target_respawn_remaining <= 0:
            self.target = TrainingTarget.ahead_of(camera)

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
        """Ažuriraj cijelu trening-borbu za jedan frame."""
        self.player.update(dt)
        self.weapons.update(dt)
        self._fire(camera, fire_primary, fire_rocket)
        self._update_projectiles(dt)
        self._hit_target()
        self._update_target_respawn(dt, camera)
        self._update_pickups(dt, camera)
