from collections.abc import Callable

import pytest

from scripts import benchmark_mode7


def test_benchmark_reports_progress() -> None:
    updates: list[float] = []

    fps = benchmark_mode7.benchmark(
        duration=0.02,
        on_progress=updates.append,
        progress_interval=0.005,
    )

    assert fps > 0
    assert updates


def test_benchmark_handles_keyboard_interrupt_without_traceback(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def interrupt(
        duration: float,
        on_progress: Callable[[float], None] | None = None,
        progress_interval: float = 10.0,
    ) -> float:
        raise KeyboardInterrupt

    monkeypatch.setattr(benchmark_mode7, "benchmark", interrupt)

    assert benchmark_mode7.run_benchmark(60, 55) == 130
    assert "cancelled" in capsys.readouterr().out
