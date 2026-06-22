from aetherfront.gameplay.projectiles import Projectile
from aetherfront.gameplay.session import CombatSession
from aetherfront.rendering.camera import Camera


def test_destroyed_target_creates_repair_and_respawns() -> None:
    camera = Camera()
    session = CombatSession.create(camera)
    session.projectiles.append(
        Projectile(
            x=session.target.x,
            y=session.target.y,
            heading=0,
            speed=0,
            damage=100,
            radius=4,
            lifetime_remaining=3,
            team="player",
            kind="rocket",
        )
    )

    session.update(0, camera)

    assert not session.target.alive
    assert len(session.pickups) == 1
    session.update(1.5, camera)
    assert session.target.alive
    assert session.target.health == 100


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
