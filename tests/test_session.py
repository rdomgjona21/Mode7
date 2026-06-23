from aetherfront.gameplay.collisions import wrapped_axis_delta
from aetherfront.gameplay.pickups import RepairPickup
from aetherfront.gameplay.projectiles import Projectile
from aetherfront.gameplay.session import CombatSession
from aetherfront.rendering.camera import Camera


def test_session_starts_with_first_configured_wave() -> None:
    camera = Camera()
    session = CombatSession.create(camera)

    assert session.wave_director.current_wave_number == 1
    assert session.enemies_remaining == 1
    assert session.enemies[0].kind.value == "scout"


def test_destroyed_enemy_awards_score_and_creates_repair() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    enemy = session.enemies[0]
    session.projectiles.append(
        Projectile(
            x=enemy.x,
            y=enemy.y,
            heading=0,
            speed=0,
            damage=enemy.max_health,
            radius=4,
            lifetime_remaining=3,
            team="player",
            kind="rocket",
        )
    )

    session.update(0, camera)

    assert enemy not in session.enemies
    assert len(session.pickups) == 1
    assert session.score == enemy.score_value
    assert session.feedback.destroyed_positions == [(enemy.x, enemy.y)]


def test_session_advances_from_first_to_second_wave_after_clear() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    session.update(3.0, camera)
    for enemy in session.enemies:
        enemy.take_damage(enemy.max_health)

    session.update(0, camera)
    assert session.enemies == []
    assert session.wave_director.incoming

    session.update(2.0, camera)
    assert session.wave_director.current_wave_number == 2
    assert session.enemies_remaining == 1
    assert session.enemies[0].kind.value == "scout"


def test_session_can_reach_waves_complete_after_clearing_three_waves() -> None:
    camera = Camera()
    session = CombatSession.create(camera)

    for wave_number in (1, 2, 3):
        session.update(10.0, camera)
        assert session.wave_director.current_wave_number == wave_number
        for enemy in session.enemies:
            enemy.take_damage(enemy.max_health)
        session.update(0.0, camera)
        if wave_number < 3:
            assert session.wave_director.incoming
            session.update(2.0, camera)

    assert session.wave_director.waves_complete
    assert session.enemies == []
    assert session.boss is not None
    assert session.boss.alive


def test_boss_receives_player_projectile_damage_after_waves() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    for wave_number in (1, 2, 3):
        session.update(10.0, camera)
        for enemy in session.enemies:
            enemy.take_damage(enemy.max_health)
        session.update(0.0, camera)
        if wave_number < 3:
            session.update(2.0, camera)
    assert session.boss is not None
    boss = session.boss
    session.projectiles.append(
        Projectile(
            x=boss.x,
            y=boss.y,
            heading=0,
            speed=0,
            damage=450,
            radius=4,
            lifetime_remaining=3,
            team="player",
            kind="rocket",
        )
    )

    session.update(0.0, camera)

    assert boss.health == 450
    assert boss.phase_label == "PHASE 2"
    assert session.feedback.boss_was_hit


def test_destroyed_boss_awards_score_and_sets_victory() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    for wave_number in (1, 2, 3):
        session.update(10.0, camera)
        for enemy in session.enemies:
            enemy.take_damage(enemy.max_health)
        session.update(0.0, camera)
        if wave_number < 3:
            session.update(2.0, camera)
    assert session.boss is not None
    boss = session.boss
    previous_score = session.score
    session.projectiles.append(
        Projectile(
            x=boss.x,
            y=boss.y,
            heading=0,
            speed=0,
            damage=boss.max_health,
            radius=4,
            lifetime_remaining=3,
            team="player",
            kind="rocket",
        )
    )

    session.update(0.0, camera)

    assert session.victory
    assert not session.game_over
    assert session.score == previous_score + boss.score_value


def test_player_death_sets_game_over() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    session.projectiles.append(
        Projectile(
            x=camera.x,
            y=camera.y,
            heading=0,
            speed=0,
            damage=session.player.max_health,
            radius=4,
            lifetime_remaining=3,
            team="enemy",
            kind="enemy_heavy",
        )
    )

    session.update(0.0, camera)

    assert session.game_over
    assert not session.victory
    assert session.feedback.player_was_damaged


def test_terminal_session_stops_updating_projectiles() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    session.victory = True
    session.feedback.player_fired = True
    session.projectiles.append(Projectile(100, 100, 0, 50, 1, 2, 3, "player"))

    session.update(1.0, camera)

    assert session.projectiles[0].x == 100
    assert session.projectiles[0].lifetime_remaining == 3
    assert not session.feedback.player_fired


def test_player_collects_repair_and_receives_score() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    session.player.take_damage(40)
    repair = session.balance.repair

    session.pickups.append(
        RepairPickup(
            x=camera.x,
            y=camera.y,
            heal_amount=repair.heal_amount,
            score_value=repair.score_value,
            radius=repair.collision_radius,
            lifetime_remaining=repair.lifetime_seconds,
        )
    )

    session.update(0, camera)

    assert session.player.health == 484
    assert session.score == 50
    assert session.pickups == []


def test_session_enforces_projectile_limit() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    projectile = Projectile(0, 0, 0, 0, 0, 1, 10, "player")
    session.projectiles = [projectile for _ in range(session.balance.projectile.limit)]

    session.update(0, camera, fire_primary=True, fire_rocket=True)

    assert len(session.projectiles) == session.balance.projectile.limit
    assert not session.feedback.player_fired


def test_session_reports_player_fired_only_when_weapon_creates_projectile() -> None:
    camera = Camera()
    session = CombatSession.create(camera)

    session.update(0, camera, fire_primary=True)
    assert session.feedback.player_fired

    session.update(0, camera, fire_primary=True)
    assert not session.feedback.player_fired


def test_enemy_projectile_can_damage_player() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    session.projectiles.append(
        Projectile(
            x=camera.x,
            y=camera.y,
            heading=0,
            speed=0,
            damage=13,
            radius=4,
            lifetime_remaining=3,
            team="enemy",
            kind="enemy_light",
        )
    )

    session.update(0, camera)

    assert session.player.health == 487
    assert session.projectiles == []


def test_enemy_behind_player_is_recycled_into_front_sector() -> None:
    camera = Camera(heading=0)
    session = CombatSession.create(camera)
    enemy = session.enemies[0]
    enemy.x = camera.x - 20
    enemy.y = camera.y

    session.update(0, camera)

    assert wrapped_axis_delta(camera.x, enemy.x) > 150
    assert session.player.health == session.player.max_health
