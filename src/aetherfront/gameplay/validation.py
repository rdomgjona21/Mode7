"""Zajedničke provjere numeričkih vrijednosti gameplay modela."""

import math
from collections.abc import Iterable


def require_finite(value: float, name: str) -> None:
    """Odbij vrijednost koja nije konačan broj."""
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def require_all_finite(values: Iterable[tuple[str, float]]) -> None:
    """Odbij prvi par čija vrijednost nije konačan broj."""
    for name, value in values:
        require_finite(value, name)


def require_positive(value: float, name: str) -> None:
    """Odbij nulu, negativne vrijednosti i beskonačnosti."""
    require_finite(value, name)
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def require_non_negative(value: float, name: str) -> None:
    """Odbij negativne vrijednosti i beskonačnosti."""
    require_finite(value, name)
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def require_text(value: str, name: str) -> None:
    """Odbij prazan tekstualni identifikator."""
    if not value:
        raise ValueError(f"{name} must not be empty")
