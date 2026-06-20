"""Izmjeri brzinu Mode7 renderera bez ograničenja na osvježavanje prozora."""

import argparse
import time

import pygame

from aetherfront.config import INTERNAL_SIZE
from aetherfront.rendering.camera import Camera
from aetherfront.rendering.renderer import Mode7Renderer


def benchmark(duration: float) -> float:
    """Renderiraj najmanje ``duration`` sekundi i vrati prosječan broj frameova."""
    if duration <= 0:
        raise ValueError("duration must be positive")

    canvas = pygame.Surface(INTERNAL_SIZE)
    camera = Camera()
    renderer = Mode7Renderer()
    frame_count = 0
    started = time.perf_counter()

    while (elapsed := time.perf_counter() - started) < duration:
        camera.update(1 / 60, turn=0.35, throttle=0.2)
        renderer.draw(canvas, camera)
        frame_count += 1

    return frame_count / elapsed


def main() -> int:
    """Pokreni benchmark i vrati pogrešku ako nije dosegnut zadani prag."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=float, default=60.0)
    parser.add_argument("--minimum", type=float, default=55.0)
    args = parser.parse_args()

    frames_per_second = benchmark(args.duration)
    print(f"Mode7 renderer: {frames_per_second:.1f} FPS over {args.duration:.1f} seconds")
    return 0 if frames_per_second >= args.minimum else 1


if __name__ == "__main__":
    raise SystemExit(main())
