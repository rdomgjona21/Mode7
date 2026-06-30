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
# Pickup sprite se u Mode7 perspektivi vidi znatno veći od osnovnog collision radiusa.
# Zato collect radius mora odgovarati vizualnom dojmu, a ne samo matematičkom sidrištu.
REPAIR_COLLECTION_RADIUS_MULTIPLIER = 10.5


@dataclass(slots=True)
class CombatFeedback:
    """Kratkotrajni događaji zadnjeg framea za vizualne povratne informacije."""

    destroyed_positions: list[tuple[float, float]] = field(default_factory=list)
    repair_collected_positions: list[tuple[float, float]] = field(default_factory=list)
    fired_weapons: list[str] = field(default_factory=list)
    enemy_fire_kinds: set[str] = field(default_factory=set)
    boss_was_hit: bool = False
    boss_spawned: bool = False
    boss_destroyed: bool = False
    wave_started: bool = False
    player_was_damaged: bool = False
    player_fired: bool = False

    def reset(self) -> None:
        """Očisti događaje prije izračuna novog framea."""
        self.destroyed_positions.clear()
        self.repair_collected_positions.clear()
        self.fired_weapons.clear()
        self.enemy_fire_kinds.clear()
        self.boss_was_hit = False
        self.boss_spawned = False
        self.boss_destroyed = False
        self.wave_started = False
        self.player_was_damaged = False
        self.player_fired = False


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
    elapsed_time: float = 0.0
    enemies_destroyed: int = 0
    repairs_collected: int = 0
    damage_taken: float = 0.0
    victory: bool = False
    game_over: bool = False
    boss_score_awarded: bool = False
    feedback: CombatFeedback = field(default_factory=CombatFeedback)

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

    def _fire(self, camera: Camera, fire_primary: bool, fire_rocket: bool) -> list[str]:
        """Dodaj projektile koje su ulazi i hlađenja dopustili u ovom frameu."""
        fired_weapons: list[str] = []
        if fire_primary:
            primary_projectiles = self.weapons.fire_primary(
                camera.x,
                camera.y,
                camera.heading,
                self._available_projectile_slots(),
            )
            self.projectiles.extend(primary_projectiles)
            if primary_projectiles:
                fired_weapons.append(self.weapons.primary.value)
        if fire_rocket:
            rocket_projectiles = self.weapons.fire_rocket(
                camera.x,
                camera.y,
                camera.heading,
                self._available_projectile_slots(),
            )
            self.projectiles.extend(rocket_projectiles)
            if rocket_projectiles:
                fired_weapons.append("rocket")
        return fired_weapons

    def _update_projectiles(self, dt: float) -> None:
        # Projektil se prvo pomakne, a zatim se neaktivni projektili uklanjaju iz liste.
        # To sprječava da istekli projektil sudjeluje u kasnijim sudarima istog framea.
        for projectile in self.projectiles:
            projectile.update(dt)
        self.projectiles = [projectile for projectile in self.projectiles if projectile.active]

    def _create_repair(self, x: float, y: float) -> None:
        # Repair pickup se stvara na mjestu uništenog standardnog protivnika.
        # Boss ne koristi ovaj sustav jer ima poseban victory reward.
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

    def _hit_enemies(self) -> list[tuple[float, float]]:
        """Primijeni prvi sudar svakog igračeva projektila s aktivnim protivnikom."""
        destroyed_positions: list[tuple[float, float]] = []
        for projectile in self.projectiles:
            if projectile.team != "player":
                continue
            for enemy in self.enemies:
                if not enemy.alive:
                    continue
                if circles_overlap(projectile.collision_body, enemy.collision_body):
                    # Jedan projektil smije pogoditi samo prvi pronađeni cilj. Zato mu se
                    # život odmah postavlja na nulu i petlja se prekida nakon obrade.
                    projectile.lifetime_remaining = 0.0
                    destroyed = enemy.take_damage(projectile.damage)
                    if destroyed:
                        # Score, telemetry, pickup i vizualni/audio feedback svi kreću iz
                        # istog događaja uništenja, pa UI i zvuk ostaju sinkronizirani.
                        self.score += enemy.score_value
                        self.enemies_destroyed += 1
                        self._create_repair(enemy.x, enemy.y)
                        destroyed_positions.append((enemy.x, enemy.y))
                    break
        self.projectiles = [projectile for projectile in self.projectiles if projectile.active]
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        return destroyed_positions

    def _hit_boss(self) -> tuple[bool, bool]:
        """Primijeni pogotke igrača na bossa i zatvori borbu nakon uništenja."""
        if self.boss is None or not self.boss.alive:
            return False, False
        boss_was_hit = False
        boss_destroyed = False
        for projectile in self.projectiles:
            if projectile.team != "player":
                continue
            if circles_overlap(projectile.collision_body, self.boss.collision_body):
                projectile.lifetime_remaining = 0.0
                destroyed = self.boss.take_damage(projectile.damage)
                boss_was_hit = True
                if destroyed and not self.boss_score_awarded:
                    # Zaštita `boss_score_awarded` sprječava dvostruko dodavanje bodova
                    # ako više projektila pogodi bossa u istom frameu.
                    self.score += self.boss.score_value
                    self.boss_score_awarded = True
                    self.victory = True
                    boss_destroyed = True
        self.projectiles = [projectile for projectile in self.projectiles if projectile.active]
        return boss_was_hit, boss_destroyed

    def _update_enemies(self, dt: float, camera: Camera) -> set[str]:
        fired_kinds: set[str] = set()
        for enemy in self.enemies:
            enemy.update(dt, camera.x, camera.y)
            if self._available_projectile_slots() <= 0:
                continue
            projectile = enemy.fire_if_ready(camera.x, camera.y)
            if projectile is not None:
                # Za audio ne treba broj svakog projektila, nego samo vrsta zvuka koja se
                # dogodila u ovom frameu. Zato se vraća set stringova.
                self.projectiles.append(projectile)
                fired_kinds.add(projectile.kind)
        return fired_kinds

    def _update_boss(self, dt: float, camera: Camera) -> set[str]:
        """Ažuriraj boss položaj i dodaj njegov burst ako je hlađenje spremno."""
        if self.boss is None or not self.boss.alive:
            return set()
        self.boss.update(dt, camera)
        available_slots = self._available_projectile_slots()
        if available_slots <= 0:
            return set()
        boss_projectiles = self.boss.fire_if_ready(camera.x, camera.y)[:available_slots]
        self.projectiles.extend(boss_projectiles)
        return {projectile.kind for projectile in boss_projectiles}

    def _ensure_boss_spawned(self, camera: Camera) -> bool:
        """Stvori ISS Goliath nakon završetka trećeg vala."""
        if not self.wave_director.waves_complete or self.boss is not None:
            return False
        self.boss = DreadnoughtBoss.spawn_ahead(camera, self.balance.boss)
        return True

    def _keep_enemies_in_front(self, camera: Camera) -> None:
        """Vrati prebliske ili iza-kamere protivnike u vidljivi prednji sektor."""
        forward_x = math.cos(camera.heading)
        forward_y = math.sin(camera.heading)
        right_x = -math.sin(camera.heading)
        right_y = math.cos(camera.heading)
        for index, enemy in enumerate(self.enemies):
            # Depth govori koliko je protivnik ispred kamere. Ako padne iza igrača ili
            # preblizu donjem rubu, vraća se u prednji sektor da borba ostane čitljiva.
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

    def _hit_player(self, camera: Camera) -> bool:
        player_body = CircleBody(camera.x, camera.y, self.balance.player.collision_radius)
        damaged = False
        for projectile in self.projectiles:
            if projectile.team != "enemy":
                continue
            if circles_overlap(player_body, projectile.collision_body):
                # `take_damage()` može odbiti štetu tijekom invulnerability prozora. Zato
                # telemetry računa samo stvarni pad healtha.
                health_before = self.player.health
                accepted = self.player.take_damage(projectile.damage)
                if accepted:
                    self.damage_taken += health_before - self.player.health
                damaged = accepted or damaged
                projectile.lifetime_remaining = 0.0
        for enemy in self.enemies:
            if circles_overlap(player_body, enemy.collision_body):
                # Kontaktna šteta koristi isti put kao projektili kako bi invulnerability
                # jednako vrijedila za sve izvore štete.
                health_before = self.player.health
                accepted = self.player.take_damage(enemy.contact_damage)
                if accepted:
                    self.damage_taken += health_before - self.player.health
                damaged = accepted or damaged
        if self.boss is not None and self.boss.alive:
            if circles_overlap(player_body, self.boss.collision_body):
                # Boss ima vlastiti veliki collision body, ali rezultat je isti događaj
                # `player_was_damaged` koji kasnije pokreće SFX i lokalni crveni marker.
                health_before = self.player.health
                accepted = self.player.take_damage(self.boss.contact_damage)
                if accepted:
                    self.damage_taken += health_before - self.player.health
                damaged = accepted or damaged
        self.projectiles = [projectile for projectile in self.projectiles if projectile.active]
        return damaged

    def _update_terminal_state(self) -> None:
        """Zaključi borbu kada igrač ostane bez trupa."""
        if not self.player.alive and not self.victory:
            self.game_over = True

    def _update_pickups(self, dt: float, camera: Camera) -> None:
        player_body = CircleBody(camera.x, camera.y, self.balance.player.collision_radius)
        for pickup in self.pickups:
            pickup.update(dt)
            collection_body = CircleBody(
                pickup.x,
                pickup.y,
                pickup.radius * REPAIR_COLLECTION_RADIUS_MULTIPLIER,
            )
            if pickup.active and circles_overlap(player_body, collection_body):
                # Repair sprite je u perspektivi velik, pa i stvarni collect radius mora
                # biti širi od modelskog radijusa. Zvuk, zeleni efekt, health i score
                # koriste isti događaj kako se povratne informacije ne bi razišle.
                _, awarded_score = pickup.collect(self.player)
                self.score += awarded_score
                self.repairs_collected += 1
                self.feedback.repair_collected_positions.append((pickup.x, pickup.y))
        self.pickups = [pickup for pickup in self.pickups if pickup.active]

    def _finalize_wave_progress(self, camera: Camera) -> None:
        """Dovrši prijelaz vala nakon što su sudari možda uklonili zadnje protivnike."""
        # Prvi `WaveDirector.update()` na početku framea koristi stvarni dt i stvara
        # protivnike čiji je delay istekao. Nakon pogodaka u istom frameu može se dogoditi
        # da je zadnji protivnik vala uništen. Ovaj drugi poziv s dt=0 ne pomiče vrijeme,
        # nego samo daje WaveDirectoru priliku da pokrene intermission ili oznaku
        # `waves_complete` odmah, bez čekanja sljedećeg framea.
        spawned_enemies = self.wave_director.update(
            0.0,
            camera,
            self.balance,
            living_enemy_count=self.enemies_remaining,
        )
        self.enemies.extend(spawned_enemies)
        self.feedback.boss_spawned = self._ensure_boss_spawned(camera) or self.feedback.boss_spawned

    def update(
        self,
        dt: float,
        camera: Camera,
        fire_primary: bool = False,
        fire_rocket: bool = False,
    ) -> None:
        """Ažuriraj trenutni testni sukob protiv standardnih protivnika."""
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("delta time must be finite and non-negative")
        self.feedback.reset()
        if self.victory or self.game_over:
            return

        # 1. Vremenski sustavi: mjerenje pokušaja, cooldowni, neranjivost i spawnovi vala.
        self.elapsed_time += dt
        self.player.update(dt)
        self.weapons.update(dt)
        previous_wave_number = self.wave_director.current_wave_number
        spawned_enemies = self.wave_director.update(
            dt,
            camera,
            self.balance,
            living_enemy_count=self.enemies_remaining,
        )
        self.enemies.extend(spawned_enemies)
        self.feedback.wave_started = (
            bool(spawned_enemies)
            and self.wave_director.current_wave_number != previous_wave_number
        )
        self.feedback.boss_spawned = self._ensure_boss_spawned(camera)

        # 2. Ulazi i AI: igrač puca, protivnici/boss se pomiču i stvaraju projektile.
        self.feedback.fired_weapons = self._fire(camera, fire_primary, fire_rocket)
        self.feedback.player_fired = bool(self.feedback.fired_weapons)
        self.feedback.enemy_fire_kinds = self._update_enemies(dt, camera)
        # Protivnici se nakon updatea recikliraju u vidljivi sektor da ih igrač ne mora
        # dugo tražiti iza kamere, što bi usporilo kratku arkadnu misiju.
        self._keep_enemies_in_front(camera)
        self.feedback.enemy_fire_kinds.update(self._update_boss(dt, camera))

        # 3. Posljedice projektila: kretanje, pogoci, šteta, score i terminalna stanja.
        self._update_projectiles(dt)
        self.feedback.destroyed_positions = self._hit_enemies()
        self.feedback.boss_was_hit, self.feedback.boss_destroyed = self._hit_boss()
        self.feedback.player_was_damaged = self._hit_player(camera)
        self._update_terminal_state()

        # 4. Završno čišćenje: val može završiti tek nakon što su pogoci uklonili neprijatelje.
        self._finalize_wave_progress(camera)
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
