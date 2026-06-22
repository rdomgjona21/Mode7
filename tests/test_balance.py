import json
from pathlib import Path

import pytest

from aetherfront.gameplay.balance import load_combat_balance


def test_default_balance_matches_locked_combat_foundation() -> None:
    balance = load_combat_balance()

    assert balance.player.max_health == 100
    assert balance.player.collision_radius == 18
    assert balance.player.invulnerability_seconds == 0.75
    assert balance.projectile.collision_radius == 4
    assert balance.projectile.lifetime_seconds == 3


def test_balance_rejects_missing_section(tmp_path: Path) -> None:
    path = tmp_path / "balance.json"
    path.write_text(json.dumps({"player": {}}), encoding="utf-8")

    with pytest.raises(ValueError, match="projectile must be an object"):
        load_combat_balance(path)


def test_balance_rejects_non_positive_number(tmp_path: Path) -> None:
    path = tmp_path / "balance.json"
    path.write_text(
        json.dumps(
            {
                "player": {
                    "max_health": 0,
                    "collision_radius": 18,
                    "invulnerability_seconds": 0.75,
                },
                "projectile": {"collision_radius": 4, "lifetime_seconds": 3},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="player.max_health"):
        load_combat_balance(path)
