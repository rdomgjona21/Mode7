import pytest

from aetherfront.gameplay.balance import load_combat_balance
from aetherfront.gameplay.weapons import PrimaryWeapon, WeaponController


def _controller() -> WeaponController:
    return WeaponController.from_balance(load_combat_balance())


def test_cannon_fires_one_projectile_and_respects_cooldown() -> None:
    controller = _controller()

    first = controller.fire_primary(100, 200, 0.5, available_slots=64)
    blocked = controller.fire_primary(100, 200, 0.5, available_slots=64)
    controller.update(0.18)
    second = controller.fire_primary(100, 200, 0.5, available_slots=64)

    assert len(first) == 1
    assert first[0].kind == "cannon"
    assert first[0].damage == 16
    assert blocked == []
    assert len(second) == 1


def test_spread_fires_three_configured_angles() -> None:
    controller = _controller()
    controller.select_primary(PrimaryWeapon.SPREAD)

    projectiles = controller.fire_primary(100, 200, 0.5, available_slots=64)

    assert len(projectiles) == 3
    assert [projectile.heading for projectile in projectiles] == pytest.approx(
        [0.34, 0.5, 0.66]
    )
    assert all(projectile.damage == 10 for projectile in projectiles)
    assert all(projectile.kind == "spread" for projectile in projectiles)


def test_rocket_has_independent_cooldown() -> None:
    controller = _controller()

    primary = controller.fire_primary(100, 200, 0, available_slots=64)
    rocket = controller.fire_rocket(100, 200, 0, available_slots=63)

    assert len(primary) == 1
    assert len(rocket) == 1
    assert rocket[0].damage == 48
    assert not controller.rocket_ready
    assert controller.fire_rocket(100, 200, 0, available_slots=64) == []


def test_weapon_does_not_exceed_available_projectile_slots() -> None:
    controller = _controller()
    controller.select_primary(PrimaryWeapon.SPREAD)

    assert controller.fire_primary(100, 200, 0, available_slots=2) == []
    assert controller.fire_rocket(100, 200, 0, available_slots=0) == []
