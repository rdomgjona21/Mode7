"""Omogući pokretanje paketa naredbom ``python -m aetherfront``."""

from aetherfront.main import main

# SystemExit pretvara povratnu vrijednost funkcije main u izlazni kod procesa.
raise SystemExit(main())
