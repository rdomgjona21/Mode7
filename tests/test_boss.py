from aetherfront.gameplay.balance import load_combat_balance
from aetherfront.gameplay.boss import BossPhase, DreadnoughtBoss
from aetherfront.rendering.camera import Camera


def _boss() -> DreadnoughtBoss:
    return DreadnoughtBoss.spawn_ahead(Camera(), load_combat_balance().boss)


def test_boss_starts_with_locked_health_and_phase_one() -> None:
    boss = _boss()

    assert boss.max_health == 900
    assert boss.health == 900
    assert boss.phase is BossPhase.PHASE_ONE
    assert boss.phase_label == "PHASE 1"


def test_boss_enters_phase_two_at_half_health() -> None:
    boss = _boss()

    boss.take_damage(450)

    assert boss.phase is BossPhase.PHASE_TWO
    assert boss.phase_label == "PHASE 2"
    assert boss.current_cooldown_seconds == 0.42


def test_boss_phase_two_fires_wider_burst() -> None:
    boss = _boss()
    boss.attack_cooldown_remaining = 0

    phase_one = boss.fire_if_ready(100, 100)
    boss.take_damage(450)
    boss.attack_cooldown_remaining = 0
    phase_two = boss.fire_if_ready(100, 100)

    assert len(phase_one) == 3
    assert len(phase_two) == 5
    assert {projectile.team for projectile in phase_two} == {"enemy"}
    assert {projectile.kind for projectile in phase_two} == {"enemy_heavy"}


def test_boss_can_be_destroyed_by_damage() -> None:
    boss = _boss()

    assert boss.take_damage(900)
    assert not boss.alive
    assert boss.phase is BossPhase.DESTROYED
