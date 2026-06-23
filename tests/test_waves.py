import json
from pathlib import Path

import pytest

from aetherfront.gameplay.balance import load_combat_balance
from aetherfront.gameplay.waves import WaveDirector, load_wave_set
from aetherfront.rendering.camera import Camera


def test_default_wave_set_has_three_ordered_waves() -> None:
    wave_set = load_wave_set()

    assert len(wave_set.waves) == 3
    assert wave_set.waves[0].name == "Scout Screen"
    assert [spawn.kind.value for spawn in wave_set.waves[0].spawns] == ["scout"] * 6
    assert {spawn.kind.value for spawn in wave_set.waves[2].spawns} == {
        "scout",
        "gunship",
        "bomber",
    }


def test_wave_spawn_delay_is_deterministic() -> None:
    director = WaveDirector(load_wave_set())
    camera = Camera()
    balance = load_combat_balance()

    first = director.update(0.0, camera, balance, living_enemy_count=0)
    early = director.update(0.39, camera, balance, living_enemy_count=1)
    second = director.update(0.01, camera, balance, living_enemy_count=1)

    assert [enemy.kind.value for enemy in first] == ["scout"]
    assert early == []
    assert [enemy.kind.value for enemy in second] == ["scout"]


def test_wave_does_not_advance_while_spawned_enemy_is_alive() -> None:
    director = WaveDirector(load_wave_set())
    camera = Camera()
    balance = load_combat_balance()

    spawned = director.update(10.0, camera, balance, living_enemy_count=0)
    director.update(0.0, camera, balance, living_enemy_count=1)

    assert len(spawned) == 6
    assert director.current_wave_number == 1
    assert not director.incoming
    assert not director.waves_complete


def test_wave_director_advances_through_all_three_waves() -> None:
    director = WaveDirector(load_wave_set())
    camera = Camera()
    balance = load_combat_balance()

    for expected_wave in (1, 2, 3):
        director.update(10.0, camera, balance, living_enemy_count=0)
        director.update(0.0, camera, balance, living_enemy_count=0)
        assert director.current_wave_number == expected_wave
        if expected_wave < 3:
            assert director.incoming
            director.update(
                director.wave_set.inter_wave_pause_seconds,
                camera,
                balance,
                living_enemy_count=0,
            )

    assert director.waves_complete
    assert director.current_wave_name == "Waves Clear"


def test_wave_loader_rejects_unsorted_spawns(tmp_path: Path) -> None:
    raw = json.loads(Path("src/aetherfront/data/waves.json").read_text(encoding="utf-8"))
    raw["waves"][0]["spawns"][0]["delay_seconds"] = 2.0
    path = tmp_path / "waves.json"
    path.write_text(json.dumps(raw), encoding="utf-8")

    with pytest.raises(ValueError, match="sorted by delay_seconds"):
        load_wave_set(path)
