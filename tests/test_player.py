import pytest

from aetherfront.gameplay.balance import load_combat_balance
from aetherfront.gameplay.player import PlayerCombatState


def _player() -> PlayerCombatState:
    return PlayerCombatState.from_balance(load_combat_balance().player)


def test_player_starts_with_full_health() -> None:
    player = _player()

    assert player.health == 100
    assert player.alive
    assert not player.invulnerable


def test_damage_starts_invulnerability_and_blocks_repeat_hit() -> None:
    player = _player()

    assert player.take_damage(25)
    assert player.health == 75
    assert player.invulnerable
    assert not player.take_damage(25)
    assert player.health == 75


def test_damage_is_allowed_after_invulnerability_expires() -> None:
    player = _player()
    player.take_damage(25)

    player.update(1.5)

    assert player.take_damage(25)
    assert player.health == 50


def test_health_is_clamped_between_zero_and_maximum() -> None:
    player = _player()
    player.take_damage(600)

    assert player.health == 0
    assert not player.alive
    assert not player.take_damage(10)
    assert player.heal(600) == 100
    assert player.health == 100


@pytest.mark.parametrize("amount", [-1, float("inf")])
def test_player_rejects_invalid_damage(amount: float) -> None:
    with pytest.raises(ValueError, match="damage"):
        _player().take_damage(amount)
