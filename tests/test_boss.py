import math

import pytest

from aetherfront.gameplay.balance import load_combat_balance
from aetherfront.gameplay.boss import BossPhase, DreadnoughtBoss
from aetherfront.rendering.camera import Camera


def _boss() -> DreadnoughtBoss:
    return DreadnoughtBoss.spawn_ahead(Camera(), load_combat_balance().boss)


def test_boss_starts_with_locked_health_and_phase_one() -> None:
    boss = _boss()

    assert boss.max_health == 1250
    assert boss.health == 1250
    assert boss.phase is BossPhase.PHASE_ONE
    assert boss.phase_label == "PHASE 1"


def test_boss_enters_phase_two_at_half_health() -> None:
    boss = _boss()

    boss.take_damage(625)

    assert boss.phase is BossPhase.PHASE_TWO
    assert boss.phase_label == "PHASE 2"
    assert boss.current_cooldown_seconds == 0.50


def test_boss_phase_two_fires_wider_burst() -> None:
    boss = _boss()
    boss.attack_cooldown_remaining = 0

    phase_one = boss.fire_if_ready(100, 100)
    boss.take_damage(625)
    boss.attack_cooldown_remaining = 0
    phase_two = boss.fire_if_ready(100, 100)

    assert len(phase_one) == 3
    assert len(phase_two) == 5
    assert {projectile.team for projectile in phase_two} == {"enemy"}
    assert {projectile.kind for projectile in phase_two} == {"enemy_heavy"}


def test_boss_can_be_destroyed_by_damage() -> None:
    boss = _boss()

    assert boss.take_damage(1250)
    assert not boss.alive
    assert boss.phase is BossPhase.DESTROYED


@pytest.mark.parametrize(
    "field, value, message",
    [
        ("max_health", 0.0, "health"),
        ("radius", 0.0, "radius"),
        ("phase_two_threshold", 1.0, "threshold"),
        ("projectile_speed", 0.0, "speed"),
        ("heading", math.inf, "finite"),
    ],
)
def test_boss_rejects_invalid_values(field: str, value: float, message: str) -> None:
    balance = load_combat_balance().boss
    values = {
        "x": 100.0,
        "y": 100.0,
        "heading": 0.0,
        "max_health": balance.max_health,
        "radius": balance.collision_radius,
        "score_value": balance.score_value,
        "contact_damage": balance.contact_damage,
        "phase_two_threshold": balance.phase_two_threshold,
        "phase_one_cooldown_seconds": balance.phase_one_cooldown_seconds,
        "phase_two_cooldown_seconds": balance.phase_two_cooldown_seconds,
        "projectile_damage": balance.projectile_damage,
        "projectile_speed": balance.projectile_speed,
        "projectile_radius": balance.projectile_radius,
        "projectile_lifetime_seconds": balance.projectile_lifetime_seconds,
    }
    values[field] = value

    with pytest.raises(ValueError, match=message):
        DreadnoughtBoss(**values)  # type: ignore[arg-type]
