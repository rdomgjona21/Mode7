from aetherfront.gameplay.balance import load_combat_balance
from aetherfront.gameplay.pickups import RepairPickup
from aetherfront.gameplay.player import PlayerCombatState


def _pickup() -> RepairPickup:
    balance = load_combat_balance().repair
    return RepairPickup(
        x=100,
        y=200,
        heal_amount=balance.heal_amount,
        score_value=balance.score_value,
        radius=balance.collision_radius,
        lifetime_remaining=balance.lifetime_seconds,
    )


def test_repair_heals_once_and_awards_score() -> None:
    balance = load_combat_balance()
    player = PlayerCombatState.from_balance(balance.player)
    player.take_damage(40)
    pickup = _pickup()

    healed, score = pickup.collect(player)

    assert healed == 24
    assert score == 50
    assert player.health == 484
    assert not pickup.active
    assert pickup.collect(player) == (0, 0)


def test_repair_expires() -> None:
    pickup = _pickup()

    assert not pickup.update(10)
    assert not pickup.active
