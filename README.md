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
- proceduralni NumPy generator teksture terena;
- vizualni Mode7 renderer s nebom, horizontom i vektoriziranim uzorkovanjem terena;
- projekcija, skaliranje i dubinsko sortiranje budućih 2D objekata u svijetu;
- proceduralni prikaz igračevog broda Kestrel;
- konfiguracijska i testirana osnova projektila, kružnih sudara, zdravlja i neranjivosti;
- skripta za 60-sekundno mjerenje performansi renderera;
- skripta za izradu i provjeru macOS `.app` paketa;
- početni automatizirani testovi i validacijska skripta.

Pucanje, vidljivi pogoci, protivnici, zvuk, testovi cijele igre, prezentacija i završni
distribucijski ZIP još nisu implementirani. Borbeni modeli trenutačno su odvojena tehnička
osnova i još nisu povezani s glavnom petljom.

Odobrenje nastavnika za temu P5 i izmijenjeni individualni raspored još treba evidentirati prije nastavka razvoja.

## Postavljanje okruženja

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m aetherfront
```

Posljednja naredba otvara vizualni Mode7 prototip. `A/D` ili strelice lijevo/desno
mijenjaju smjer, a `W/S` ili strelice gore/dolje mijenjaju brzinu. Nebo, horizont i
proceduralni teren reagiraju na kameru, a Kestrel je vidljiv pri dnu zaslona; borba još
nije implementirana.

Provjera koda i testova pokreće se naredbom:

```bash
./scripts/validate.sh
```

Izolirano 60-sekundno mjerenje Mode7 renderera pokreće se naredbom:

```bash
python scripts/benchmark_mode7.py --duration 60 --minimum 55
```

Rana macOS aplikacija izrađuje se u ignoriranoj mapi `dist/`:

```bash
./scripts/package.sh
open dist/Aetherfront.app
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
