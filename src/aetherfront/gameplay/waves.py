"""Konfigurirani valovi standardnih protivnika."""

import json
import math
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any

from aetherfront.config import WORLD_SIZE
from aetherfront.gameplay.balance import CombatBalance
from aetherfront.gameplay.enemies import Enemy, EnemyKind
from aetherfront.rendering.camera import Camera


@dataclass(frozen=True, slots=True)
class WaveSpawn:
    """Jedan konfigurirani spawn unutar vala."""

    kind: EnemyKind
    delay_seconds: float
    forward: float
    side: float
    attack_cooldown_factor: float


@dataclass(frozen=True, slots=True)
class WaveConfig:
    """Jedan val s čitljivim nazivom i popisom spawnova."""

    name: str
    spawns: tuple[WaveSpawn, ...]


@dataclass(frozen=True, slots=True)
class WaveSet:
    """Cijela konfiguracija redovnih valova za misiju."""

    inter_wave_pause_seconds: float
    waves: tuple[WaveConfig, ...]


def _positive_number(section: dict[str, Any], key: str, section_name: str) -> float:
    value = section.get(key)
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{section_name}.{key} must be a positive number")
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise ValueError(f"{section_name}.{key} must be a positive number")
    return result


def _non_negative_number(section: dict[str, Any], key: str, section_name: str) -> float:
    value = section.get(key)
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{section_name}.{key} must be a non-negative number")
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"{section_name}.{key} must be a non-negative number")
    return result


def _finite_number(section: dict[str, Any], key: str, section_name: str) -> float:
    value = section.get(key)
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{section_name}.{key} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{section_name}.{key} must be a finite number")
    return result


def _object(value: Any, section_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{section_name} must be an object")
    return value


def _spawn(raw: Any, section_name: str) -> WaveSpawn:
    section = _object(raw, section_name)
    try:
        kind = EnemyKind(section.get("kind"))
    except ValueError as error:
        raise ValueError(f"{section_name}.kind must be scout, gunship or bomber") from error
    return WaveSpawn(
        kind=kind,
        delay_seconds=_non_negative_number(section, "delay_seconds", section_name),
        forward=_positive_number(section, "forward", section_name),
        side=_finite_number(section, "side", section_name),
        attack_cooldown_factor=_non_negative_number(
            section,
            "attack_cooldown_factor",
            section_name,
        ),
    )


def _wave(raw: Any, index: int) -> WaveConfig:
    section_name = f"waves[{index}]"
    section = _object(raw, section_name)
    name = section.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"{section_name}.name must be a non-empty string")
    raw_spawns = section.get("spawns")
    if not isinstance(raw_spawns, list) or not raw_spawns:
        raise ValueError(f"{section_name}.spawns must be a non-empty array")
    spawns = tuple(
        _spawn(raw_spawn, f"{section_name}.spawns[{i}]")
        for i, raw_spawn in enumerate(raw_spawns)
    )
    delays = [spawn.delay_seconds for spawn in spawns]
    if delays != sorted(delays):
        raise ValueError(f"{section_name}.spawns must be sorted by delay_seconds")
    return WaveConfig(name=name, spawns=spawns)


def load_wave_set(path: Path | None = None) -> WaveSet:
    """Učitaj zadane valove iz paketa ili testnu JSON datoteku."""
    if path is None:
        resource = files("aetherfront").joinpath("data/waves.json")
        with resource.open(encoding="utf-8") as handle:
            raw = json.load(handle)
    else:
        with path.open(encoding="utf-8") as handle:
            raw = json.load(handle)

    root = _object(raw, "waves root")
    raw_waves = root.get("waves")
    if not isinstance(raw_waves, list) or len(raw_waves) != 3:
        raise ValueError("waves must contain exactly three waves")
    return WaveSet(
        inter_wave_pause_seconds=_positive_number(
            root,
            "inter_wave_pause_seconds",
            "waves root",
        ),
        waves=tuple(_wave(raw_wave, index) for index, raw_wave in enumerate(raw_waves)),
    )


@dataclass(slots=True)
class WaveDirector:
    """Prati redovne valove, spawn odgode i stanke između valova."""

    wave_set: WaveSet
    wave_index: int = 0
    time_in_wave: float = 0.0
    next_spawn_index: int = 0
    intermission_remaining: float = 0.0
    waves_complete: bool = False

    @classmethod
    def create(cls) -> "WaveDirector":
        """Stvori direktor iz zadane paketne konfiguracije."""
        return cls(load_wave_set())

    @property
    def total_waves(self) -> int:
        """Ukupan broj redovnih valova."""
        return len(self.wave_set.waves)

    @property
    def current_wave_number(self) -> int:
        """Trenutačni val kao broj za HUD, od 1 do ukupnog broja valova."""
        if self.waves_complete:
            return self.total_waves
        return min(self.wave_index + 1, self.total_waves)

    @property
    def current_wave_name(self) -> str:
        """Čitljiv naziv trenutačnog vala ili završnog stanja."""
        if self.waves_complete:
            return "Waves Clear"
        return self.wave_set.waves[self.wave_index].name

    @property
    def incoming(self) -> bool:
        """Je li igra u stanci između očišćenog i sljedećeg vala."""
        return self.intermission_remaining > 0

    def _current_wave(self) -> WaveConfig:
        return self.wave_set.waves[self.wave_index]

    def _current_wave_cleared(self, living_enemy_count: int) -> bool:
        return self.next_spawn_index >= len(self._current_wave().spawns) and living_enemy_count == 0

    def _start_next_state(self) -> None:
        if self.wave_index >= self.total_waves - 1:
            self.waves_complete = True
            return
        self.intermission_remaining = self.wave_set.inter_wave_pause_seconds

    def _begin_next_wave(self) -> None:
        self.wave_index += 1
        if self.wave_index >= self.total_waves:
            self.waves_complete = True
            return
        self.time_in_wave = 0.0
        self.next_spawn_index = 0

    def _spawn_ready(self, camera: Camera, balance: CombatBalance) -> list[Enemy]:
        spawned: list[Enemy] = []
        spawns = self._current_wave().spawns
        while self.next_spawn_index < len(spawns):
            spawn = spawns[self.next_spawn_index]
            if spawn.delay_seconds > self.time_in_wave:
                break
            spawned.append(_create_enemy_from_spawn(spawn, camera, balance))
            self.next_spawn_index += 1
        return spawned

    def update(
        self,
        dt: float,
        camera: Camera,
        balance: CombatBalance,
        living_enemy_count: int,
    ) -> list[Enemy]:
        """Ažuriraj valove i vrati protivnike koji trebaju nastati u ovom frameu."""
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("delta time must be finite and non-negative")
        if living_enemy_count < 0:
            raise ValueError("living enemy count must not be negative")
        if self.waves_complete:
            return []

        if self.intermission_remaining > 0:
            self.intermission_remaining = max(0.0, self.intermission_remaining - dt)
            if self.intermission_remaining > 0:
                return []
            self._begin_next_wave()
            if self.waves_complete:
                return []
            return self._spawn_ready(camera, balance)

        if self._current_wave_cleared(living_enemy_count):
            self._start_next_state()
            return []

        self.time_in_wave += dt
        return self._spawn_ready(camera, balance)


def _create_enemy_from_spawn(
    spawn: WaveSpawn,
    camera: Camera,
    balance: CombatBalance,
) -> Enemy:
    """Pretvori konfigurirani spawn u protivnika relativno na kameru."""
    forward_x = math.cos(camera.heading)
    forward_y = math.sin(camera.heading)
    right_x = -math.sin(camera.heading)
    right_y = math.cos(camera.heading)
    x = (camera.x + forward_x * spawn.forward + right_x * spawn.side) % WORLD_SIZE
    y = (camera.y + forward_y * spawn.forward + right_y * spawn.side) % WORLD_SIZE
    enemy_balance = balance.enemies[spawn.kind.value]
    return Enemy.from_balance(
        spawn.kind,
        enemy_balance,
        x,
        y,
        heading=(camera.heading + math.pi) % math.tau,
        attack_cooldown_remaining=enemy_balance.attack_cooldown_seconds
        * spawn.attack_cooldown_factor,
    )
