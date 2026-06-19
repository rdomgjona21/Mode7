"""Application entry point."""

from aetherfront.core.game import Game


def main() -> int:
    """Start the technical prototype."""
    return Game().run()


if __name__ == "__main__":
    raise SystemExit(main())
