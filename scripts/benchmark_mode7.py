"""Izmjeri brzinu Mode7 renderera bez ograničenja na osvježavanje prozora."""

import argparse
import time
from collections.abc import Callable

import pygame

from aetherfront.config import INTERNAL_SIZE
from aetherfront.rendering.camera import Camera
from aetherfront.rendering.renderer import Mode7Renderer


def benchmark(
    duration: float,
    on_progress: Callable[[float], None] | None = None,
    progress_interval: float = 10.0,
) -> float:
    """Renderiraj najmanje ``duration`` sekundi i vrati prosječan broj frameova."""
    if duration <= 0:
        raise ValueError("duration must be positive")
    if progress_interval <= 0:
        raise ValueError("progress interval must be positive")

    canvas = pygame.Surface(INTERNAL_SIZE)
    camera = Camera()
    renderer = Mode7Renderer()
    frame_count = 0
    started = time.perf_counter()
    next_progress = min(progress_interval, duration)
    last_reported_progress = 0.0

    while (elapsed := time.perf_counter() - started) < duration:
        camera.update(1 / 60, turn=0.35, throttle=0.2)
        renderer.draw(canvas, camera)
        frame_count += 1
        if on_progress is not None and elapsed >= next_progress:
            reported_progress = min(elapsed, duration)
            on_progress(reported_progress)
            last_reported_progress = reported_progress
            next_progress += progress_interval

    final_progress = min(elapsed, duration)
    if on_progress is not None and final_progress > last_reported_progress:
        on_progress(final_progress)

    return frame_count / elapsed


def run_benchmark(duration: float, minimum: float) -> int:
    """Izvedi mjerenje, ispiši napredak i uredno obradi prekid korisnika."""
    try:
        frames_per_second = benchmark(
            duration,
            on_progress=lambda elapsed: print(
                f"Benchmark progress: {min(elapsed, duration):.0f}/{duration:.0f} seconds"
            ),
        )
    except KeyboardInterrupt:
        print("\nBenchmark cancelled before completion.")
        return 130

    print(f"Mode7 renderer: {frames_per_second:.1f} FPS over {duration:.1f} seconds")
    return 0 if frames_per_second >= minimum else 1


def main() -> int:
    """Pokreni benchmark i vrati pogrešku ako nije dosegnut zadani prag."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=float, default=60.0)
    parser.add_argument("--minimum", type=float, default=55.0)
    args = parser.parse_args()

    return run_benchmark(args.duration, args.minimum)


if __name__ == "__main__":
    raise SystemExit(main())
