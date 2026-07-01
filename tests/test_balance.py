import json
from pathlib import Path

import pytest

from aetherfront.gameplay.balance import load_combat_balance


def test_default_balance_matches_locked_combat_foundation() -> None:
    balance = load_combat_balance()

    assert balance.player.max_health == 100
    assert balance.player.collision_radius == 18
    assert balance.player.invulnerability_seconds == 1.25
    assert balance.projectile.collision_radius == 4
    assert balance.projectile.lifetime_seconds == 3
    assert balance.projectile.limit == 64
    assert balance.cannon.damage == 18
    assert balance.cannon.cooldown_seconds == 0.20
    assert balance.spread.damage == 9
    assert balance.spread.angle_offsets == (-0.16, 0.0, 0.16)
    assert balance.rocket.damage == 62
    assert balance.rocket.cooldown_seconds == 1.35
    assert balance.repair.heal_amount == 36
    assert balance.repair.score_value == 75
    assert set(balance.enemies) == {"scout", "gunship", "bomber"}
    assert balance.enemies["scout"].max_health == 32
    assert balance.enemies["gunship"].score_value == 240
    assert balance.enemies["bomber"].projectile_damage == 24
    assert balance.boss.max_health == 1250
    assert balance.boss.score_value == 5000
    assert balance.boss.phase_two_threshold == 0.5


def test_balance_rejects_missing_section(tmp_path: Path) -> None:
    path = tmp_path / "balance.json"
    path.write_text(json.dumps({"player": {}}), encoding="utf-8")

    with pytest.raises(ValueError, match="projectile must be an object"):
        load_combat_balance(path)


def test_balance_rejects_non_positive_number(tmp_path: Path) -> None:
    path = tmp_path / "balance.json"
    raw = json.loads(Path("src/aetherfront/data/balance.json").read_text(encoding="utf-8"))
    raw["player"]["max_health"] = 0
    path.write_text(json.dumps(raw), encoding="utf-8")

    with pytest.raises(ValueError, match="player.max_health"):
        load_combat_balance(path)
