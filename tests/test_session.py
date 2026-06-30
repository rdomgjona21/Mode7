import pytest

from aetherfront.gameplay.collisions import wrapped_axis_delta
from aetherfront.gameplay.pickups import RepairPickup
from aetherfront.gameplay.projectiles import Projectile
from aetherfront.gameplay.session import (
    REPAIR_COLLECTION_RADIUS_MULTIPLIER,
    CombatSession,
)
from aetherfront.rendering.camera import Camera


def test_session_starts_with_first_configured_wave() -> None:
    camera = Camera()
    session = CombatSession.create(camera)

    assert session.wave_director.current_wave_number == 1
    assert session.enemies_remaining == 1
    assert session.enemies[0].kind.value == "scout"


def test_combat_feedback_deduplicates_enemy_fire_kinds() -> None:
    session = CombatSession.create(Camera())

    session.feedback.enemy_fire_kinds.update(("enemy_light", "enemy_light", "enemy_heavy"))

    assert session.feedback.enemy_fire_kinds == {"enemy_light", "enemy_heavy"}


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
    assert session.enemies_destroyed == 1
    assert session.feedback.destroyed_positions == [(enemy.x, enemy.y)]


def test_session_tracks_elapsed_time_only_while_active() -> None:
    camera = Camera()
    session = CombatSession.create(camera)

    session.update(1.25, camera)
    session.update(0.75, camera)
    session.victory = True
    session.update(5.0, camera)

    assert session.elapsed_time == pytest.approx(2.0)


def test_session_rejects_invalid_delta_time_before_telemetry_changes() -> None:
    camera = Camera()
    session = CombatSession.create(camera)

    with pytest.raises(ValueError, match="delta time"):
        session.update(-0.1, camera)

    assert session.elapsed_time == 0.0


def test_session_advances_from_first_to_second_wave_after_clear() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    session.update(3.0, camera)
    for enemy in session.enemies:
        enemy.take_damage(enemy.max_health)

    session.update(0, camera)
    assert session.enemies == []
    assert session.wave_director.incoming

    session.update(2.4, camera)
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
            session.update(2.4, camera)

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
            session.update(2.4, camera)
    assert session.boss is not None
    boss = session.boss
    session.projectiles.append(
        Projectile(
            x=boss.x,
            y=boss.y,
            heading=0,
            speed=0,
            damage=625,
            radius=4,
            lifetime_remaining=3,
            team="player",
            kind="rocket",
        )
    )

    session.update(0.0, camera)

    assert boss.health == 625
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
            session.update(2.4, camera)
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
    assert session.damage_taken == session.player.max_health


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

    assert session.player.health == 446
    assert session.score == 75
    assert session.pickups == []
    assert session.repairs_collected == 1
    assert session.feedback.repair_collected_positions == [(camera.x, camera.y)]


def test_player_collects_repair_when_touching_visible_pickup_edge() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    repair = session.balance.repair
    player_radius = session.balance.player.collision_radius
    x_offset = player_radius + repair.collision_radius * REPAIR_COLLECTION_RADIUS_MULTIPLIER - 1

    session.pickups.append(
        RepairPickup(
            x=camera.x + x_offset,
            y=camera.y,
            heal_amount=repair.heal_amount,
            score_value=repair.score_value,
            radius=repair.collision_radius,
            lifetime_remaining=repair.lifetime_seconds,
        )
    )

    session.update(0, camera)

    assert session.pickups == []
    assert session.repairs_collected == 1
    assert session.feedback.repair_collected_positions == [(camera.x + x_offset, camera.y)]


def test_repair_feedback_uses_single_early_collection_event() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    repair = session.balance.repair
    player_radius = session.balance.player.collision_radius
    pickup_offset = (
        player_radius
        + repair.collision_radius * REPAIR_COLLECTION_RADIUS_MULTIPLIER
        - 1
    )

    session.pickups.append(
        RepairPickup(
            x=camera.x + pickup_offset,
            y=camera.y,
            heal_amount=repair.heal_amount,
            score_value=repair.score_value,
            radius=repair.collision_radius,
            lifetime_remaining=repair.lifetime_seconds,
        )
    )

    session.update(0, camera)

    assert session.pickups == []
    assert session.repairs_collected == 1
    assert session.feedback.repair_collected_positions == [(camera.x + pickup_offset, camera.y)]


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
    assert session.feedback.fired_weapons == ["cannon"]

    session.update(0, camera, fire_primary=True)
    assert not session.feedback.player_fired
    assert session.feedback.fired_weapons == []


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

    assert session.player.health == 437
    assert session.projectiles == []
    assert session.damage_taken == 13
    assert session.feedback.player_was_damaged


def test_enemy_behind_player_is_recycled_into_front_sector() -> None:
    camera = Camera(heading=0)
    session = CombatSession.create(camera)
    enemy = session.enemies[0]
    enemy.x = camera.x - 20
    enemy.y = camera.y

    session.update(0, camera)

    assert wrapped_axis_delta(camera.x, enemy.x) > 150
    assert session.player.health == session.player.max_health
