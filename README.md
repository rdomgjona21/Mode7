# Aetherfront: Zeppelin Wars

Početna struktura individualnog projekta P5 — Mode7 / pucačina.

## Trenutačni status

Projekt se nalazi na početku tehničke implementacije. Dovršeni su:

- početna struktura mapa;
- projektni plan;
- početna verzija dokumenta dizajna igre;
- Python virtualno okruženje;
- konfiguracija paketa Python 3.12, PyGame, NumPy, Ruff, Pytest i PyInstaller;
- osnovni PyGame prozor, glavna petlja i skaliranje interne slike;
- kamera s upravljanjem, brzinom i omatanjem svijeta;
- vektorizirana Mode7 projekcijska matematika;
- početni automatizirani testovi i validacijska skripta.

Gameplay, vizualni Mode7 prikaz, protivnici, zvuk, testovi igre, prezentacija i distribucijski paket još nisu implementirani.

Odobrenje nastavnika za temu P5 i izmijenjeni individualni raspored još treba evidentirati prije nastavka razvoja.

## Postavljanje okruženja

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m aetherfront
```

Posljednja naredba otvara tehnički prototip kamere. `A/D` ili strelice lijevo/desno mijenjaju smjer, a `W/S` ili strelice gore/dolje mijenjaju brzinu. Trenutačne vrijednosti prikazane su u prozoru; Mode7 i gameplay još nisu implementirani.

Provjera koda i testova pokreće se naredbom:

```bash
./scripts/validate.sh
```

## Dokumentacija

- [Aktivni operativni plan do 2. srpnja](docs/execution-plan-to-july-2.md)
- [Projektni plan](docs/project-plan.md)
- [Početni dokument dizajna igre](docs/gdd.md)
- [Tehnička dokumentacija](docs/technical-documentation.md)
- [Vodič kroz trenutačni kod](docs/code-walkthrough.md)
- [Evidencija uporabe AI-ja](docs/ai-usage.md)

Dokumentacija je na hrvatskom. Planirani tekst unutar igre i završna prezentacija bit će na engleskom.

## Licenca

Izvorni kod objavit će se pod licencom MIT. Pogledajte [LICENSE](LICENSE).
