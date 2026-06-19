# Aetherfront: Zeppelin Wars

Početna struktura individualnog projekta P5 — Mode7 / pucačina.

## Trenutačni status

Projekt se nalazi na kraju faze inicijalizacije. Dovršeni su:

- početna struktura mapa;
- projektni plan;
- početna verzija dokumenta dizajna igre;
- Python virtualno okruženje;
- konfiguracija paketa Python 3.12, PyGame, NumPy, Ruff, Pytest i PyInstaller.

Gameplay, Mode7 prikaz, protivnici, zvuk, testovi igre, prezentacija i distribucijski paket još nisu implementirani.

Odobrenje nastavnika za temu P5 i izmijenjeni individualni raspored još treba evidentirati prije nastavka razvoja.

## Postavljanje okruženja

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m aetherfront
```

Posljednja naredba samo provjerava instalirane razvojne ovisnosti; ne pokreće igru.

## Dokumentacija

- [Projektni plan](docs/project-plan.md)
- [Početni dokument dizajna igre](docs/gdd.md)

Dokumentacija je na hrvatskom. Planirani tekst unutar igre i završna prezentacija bit će na engleskom.

## Licenca

Izvorni kod objavit će se pod licencom MIT. Pogledajte [LICENSE](LICENSE).
