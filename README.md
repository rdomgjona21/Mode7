# Aetherfront: Zeppelin Wars

Individualni projekt P5 — Mode7 / pucačina.

## Trenutačni status

Projekt je u fazi igrive borbene probe. Dovršeni su:

- početna struktura mapa;
- projektni plan;
- početna verzija dokumenta dizajna igre;
- Python virtualno okruženje;
- konfiguracija paketa Python 3.12, PyGame, NumPy, Ruff, Pytest i PyInstaller;
- osnovni PyGame prozor, glavna petlja i skaliranje interne slike;
- kamera s upravljanjem, brzinom i omatanjem svijeta;
- vektorizirana Mode7 projekcijska matematika;
- generirani cloud PNG asset s proceduralnim fallbackom za Mode7 podlogu;
- vizualni Mode7 renderer s nebom, horizontom i vektoriziranim uzorkovanjem terena;
- proceduralni parallax sky slojevi s oblacima, balonima i lebdećom gradskom siluetom;
- projekcija, skaliranje i dubinsko sortiranje budućih 2D objekata u svijetu;
- proceduralni Victorian airship prikaz igračevog broda Kestrel;
- konfiguracijska i testirana osnova projektila, kružnih sudara, zdravlja i neranjivosti;
- cannon, spread gun i rakete s vidljivim projektilima i hlađenjem;
- scout, gunship i bomber s kretanjem, zdravljem, napadima, proceduralnim viktorijanskim
  airship oblicima i bodovima;
- `waves.json` i `WaveDirector` s tri konfigurirana redovna vala;
- ISS Goliath boss s masivnijim viktorijanskim dreadnought prikazom, dvije faze, burst
  paljbom i boss HUD-om;
- repair pickup i minimalistički steampunk engleski HUD s prikazom protivnika;
- glavni izbornik, ekran uputa, pauza te restart ili povratak u izbornik nakon završetka;
- suptilni proceduralni visual feedback za pucanje, pogotke, štetu, skupljanje popravka i
  uništenje protivnika;
- ElevenLabs zvučni efekti za oružja, protivnike, bossa, repair pickup, UI, pobjedu i
  game-over stanje;
- generirana WAV glazbena podloga za menu, tri redovna vala i dvije boss faze;
- osnovna balance telemetry mjerenja: vrijeme pokušaja, uništeni protivnici, skupljeni
  popravci i primljena šteta;
- skripta za 60-sekundno mjerenje performansi renderera;
- skripta za izradu i provjeru macOS `.app` paketa;
- početni automatizirani testovi, validacijska skripta i obrazac ručnog playtesta.

Tri oružja, vidljivi pogoci i suptilni proceduralni efekti sada rade kroz tri konfigurirana
redovna vala, boss susret, pobjedu i game-over stanje. Aplikacija ima tok od glavnog
izbornika do završetka pokušaja. Parallax sky slojevi sada se suptilno pomiču sporije od
kamere iznad horizonta. Prvi završni balance pass, minimalistički steampunk HUD, zvučni
efekti i glazbena podloga su implementirani. Završni ručni playtestovi, prezentacija i
završni distribucijski ZIP još nisu implementirani.

Odobrenje nastavnika za temu P5 i izmijenjeni individualni raspored zaprimljeno je i
evidentirano 22. lipnja 2026.

## Postavljanje okruženja

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m aetherfront
```

Posljednja naredba otvara glavni izbornik. `Enter` ili `Space` pokreće misiju, `I`
otvara upute, a `Esc` zatvara aplikaciju iz glavnog izbornika. U igri `A/D` ili strelice
lijevo/desno mijenjaju smjer, a `W/S` ili strelice gore/dolje mijenjaju brzinu. `1/2`
bira cannon ili spread gun, `Space` puca, lijevi ili desni `Shift` ispaljuje raketu, a
`Esc` pauzira. Nakon pobjede ili poraza `R` pokreće novi pokušaj, a `M` vraća na izbornik.

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
- [Izvještaj o testiranju](docs/testing-report.md)
- [Evidencija uporabe AI-ja](docs/ai-usage.md)

Dokumentacija je na hrvatskom. Planirani tekst unutar igre i završna prezentacija bit će na engleskom.

## Licenca

Izvorni kod objavit će se pod licencom MIT. Pogledajte [LICENSE](LICENSE).
