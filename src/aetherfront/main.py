"""Ulazna točka aplikacije."""

from aetherfront.core.game import Game


def main() -> int:
    """Stvori igru i vrati njezin izlazni kod operacijskom sustavu."""
    return Game().run()


# Ovaj uvjet vrijedi kada se datoteka pokrene izravno, ali ne i kada se uveze u test.
if __name__ == "__main__":
    raise SystemExit(main())
