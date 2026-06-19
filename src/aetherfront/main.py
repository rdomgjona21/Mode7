"""Development-environment verification entry point."""

import numpy
import pygame


def main() -> int:
    """Report configured dependencies without starting gameplay."""
    print("Aetherfront development environment is configured.")
    print(f"PyGame {pygame.version.ver}")
    print(f"NumPy {numpy.__version__}")
    print("Gameplay has not been implemented yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
