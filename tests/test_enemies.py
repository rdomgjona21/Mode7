import math

from aetherfront.gameplay.balance import load_combat_balance
from aetherfront.gameplay.enemies import Enemy, EnemyKind


def _enemy(kind: EnemyKind = EnemyKind.SCOUT) -> Enemy:
    balance = load_combat_balance().enemies[kind.value]
    return Enemy.from_balance(kind, balance, x=100, y=100)


def test_enemy_kinds_have_distinct_locked_balance_values() -> None:
    balance = load_combat_balance()

    assert balance.enemies["scout"].max_health < balance.enemies["gunship"].max_health
    assert balance.enemies["gunship"].max_health < balance.enemies["bomber"].max_health
    assert balance.enemies["scout"].speed > balance.enemies["gunship"].speed
    assert balance.enemies["bomber"].score_value == 420


def test_enemy_takes_damage_and_reports_death_once() -> None:
    enemy = _enemy(EnemyKind.GUNSHIP)

    assert not enemy.take_damage(20)
    assert enemy.alive
    assert enemy.take_damage(100)
    assert not enemy.alive
    assert not enemy.take_damage(100)


def test_enemy_movement_is_deterministic_across_frame_division() -> None:
    one_step = _enemy(EnemyKind.BOMBER)
    two_steps = _enemy(EnemyKind.BOMBER)

    one_step.update(1.0, player_x=300, player_y=100)
    two_steps.update(0.5, player_x=300, player_y=100)
    two_steps.update(0.5, player_x=300, player_y=100)

    assert math.isclose(one_step.x, two_steps.x, abs_tol=2.0)
    assert math.isclose(one_step.y, two_steps.y, abs_tol=2.0)


def test_enemy_projectile_respects_attack_cooldown() -> None:
    enemy = _enemy(EnemyKind.BOMBER)

    first = enemy.fire_if_ready(player_x=120, player_y=100)
    second = enemy.fire_if_ready(player_x=120, player_y=100)

    assert first is not None
    assert first.team == "enemy"
    assert first.kind == "enemy_heavy"
    assert second is None
