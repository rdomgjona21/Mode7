from aetherfront.gameplay.projectiles import Projectile
from aetherfront.gameplay.session import CombatSession
from aetherfront.rendering.camera import Camera


def test_session_starts_with_three_standard_enemy_types() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    kinds = {enemy.kind.value for enemy in session.enemies}

    assert kinds == {"scout", "gunship", "bomber"}
    assert session.enemies_remaining == 4


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


def test_enemy_group_respawns_after_all_enemies_are_destroyed() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    for enemy in session.enemies:
        enemy.take_damage(enemy.max_health)

    session.update(0, camera)
    assert session.enemies == []
    assert session.enemy_group_respawn_remaining > 0

    session.update(2.0, camera)
    assert session.enemies_remaining == 4


def test_player_collects_repair_and_receives_score() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    session.player.take_damage(40)
    repair = session.balance.repair
    from aetherfront.gameplay.pickups import RepairPickup

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

    assert session.player.health == 84
    assert session.score == 50
    assert session.pickups == []


def test_session_enforces_projectile_limit() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    projectile = Projectile(0, 0, 0, 0, 0, 1, 10, "player")
    session.projectiles = [projectile for _ in range(session.balance.projectile.limit)]

    session.update(0, camera, fire_primary=True, fire_rocket=True)

    assert len(session.projectiles) == session.balance.projectile.limit


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

    assert session.player.health == 87
    assert session.projectiles == []
