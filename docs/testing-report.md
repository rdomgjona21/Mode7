# Izvještaj o testiranju — Aetherfront: Zeppelin Wars

**Status:** release kandidat; automatizirane provjere i 5+ ručnih sesija prolaze  
**Datum početka:** 24. lipnja 2026.  
**Zadnje ažuriranje:** 2. srpnja 2026.

## 1. Svrha

Ovaj izvještaj bilježi automatizirane provjere, ručne playtest sesije i odluke o
balansiranju. Cilj je dokazati da je vertikalni presjek stabilan, čitljiv, dovoljno
izazovan i spreman za završni release kandidat.

## 2. Automatizirane provjere

Standardna provjera pokreće se naredbom:

```bash
./scripts/validate.sh
```

Trenutačni skup pokriva konfiguraciju, kameru, Mode7 projekciju, renderer, billboarde,
oružja, protivnike, valove, bossa, HUD, efekte, audio assete, pickupove, borbenu sesiju i
benchmark skriptu.

Završna provjera 2. srpnja 2026. pokrenuta je na commitu `58e9649`:

```bash
PATH=.venv/bin:$PATH ./scripts/validate.sh
```

Rezultat:

```text
All checks passed!
190 passed
```

## 3. Performanse

Izolirano mjerenje renderera pokreće se naredbom:

```bash
python scripts/benchmark_mode7.py --duration 12 --minimum 55
```

Prag prihvata ostaje najmanje 55 FPS. Završno mjerenje potrebno je ponoviti nakon
balansiranja i prije izrade release ZIP-a.

Završno mjerenje za release kandidata 2. srpnja 2026.:

```bash
PATH=.venv/bin:$PATH python scripts/benchmark_mode7.py --duration 12 --minimum 55
```

Rezultat:

```text
Mode7 renderer: 159.9 FPS over 12.0 seconds
```

Izmjereni rezultat je iznad praga od 55 FPS.

## 4. Ručni playtestovi

Za svaku potpunu sesiju treba ispuniti `tests/playtest-notes.md`. U izvještaj se zatim
prepisuju sažeci najvažnijih rezultata: trajanje, ishod, score, skupljeni repair pickupovi,
primljena šteta, dojam težine i pronađeni problemi.

Autor je 2. srpnja 2026. potvrdio da je odigrao više od pet potpunih sesija i da se igra
ponašala stabilno. Detaljne telemetry vrijednosti iz HUD-a nisu zapisane za svaku sesiju,
pa se u tablici ne izmišljaju precizni score, damage i repair brojevi. Za završnu predaju
relevantna je potvrda da je cjelovit tok igre ponovljivo odigran bez neobrađene iznimke.

| # | Datum | Commit | Ishod | Vrijeme | Score | Damage | Repairs | Napomena |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | 2. 7. 2026. | `58e9649` | završena sesija | nije zapisano | nije zapisano | nije zapisano | nije zapisano | Menu, gameplay, valovi, boss i završni ekran rade bez rušenja. |
| 2 | 2. 7. 2026. | `58e9649` | završena sesija | nije zapisano | nije zapisano | nije zapisano | nije zapisano | Pauza, nastavak igre, restart i povratak u izbornik provjereni. |
| 3 | 2. 7. 2026. | `58e9649` | završena sesija | nije zapisano | nije zapisano | nije zapisano | nije zapisano | Vidljivi su sva tri oružja, tri vrste protivnika i repair pickup. |
| 4 | 2. 7. 2026. | `58e9649` | završena sesija | nije zapisano | nije zapisano | nije zapisano | nije zapisano | Boss phase 2, boss HUD, glazba i SFX rade tijekom završnice. |
| 5 | 2. 7. 2026. | `58e9649` | završena sesija | nije zapisano | nije zapisano | nije zapisano | nije zapisano | Nije primijećena neobrađena iznimka, zamrzavanje ni prekid aplikacije. |

Sažetak ručnih provjera:

- Igra se pokreće iz izvornog koda naredbom `python -m aetherfront`.
- Glavni izbornik, upute, aktivna igra, pauza i završni ekrani rade očekivano.
- Tri konfigurirana vala pojavljuju se redom i vode do boss susreta.
- ISS Goliath ima dvije faze; phase 2 i boss health bar vidljivi su u normalnom igranju.
- Cannon, spread gun i rockets stvaraju vidljive projektile i zvučne efekte.
- Repair pickup vraća health i pokreće zeleni/cijan vizualni feedback.
- Menu, valovi i boss faze imaju čujnu glazbenu podlogu.
- U pet i više ručnih sesija nije zabilježena neobrađena iznimka.

## 5. Kriteriji prihvata

- Igra se pokreće iz izvornog koda.
- Moguće je doći od glavnog izbornika do pobjede ili game-over stanja.
- Pauza, restart, povratak u izbornik i izlaz rade bez rušenja.
- Svako oružje, svaki standardni protivnik, repair pickup i obje faze bossa vidljivi su u
  uobičajenoj sesiji.
- Skupljanje repair pickupa prikazuje kratki zeleni vizualni feedback bez prekrivanja HUD-a.
- Pucanje, protivnici, boss, repair, UI, pobjeda i game-over imaju čitljive zvučne efekte.
- Menu, tri redovna vala i dvije boss faze imaju različite generirane WAV glazbene loopove.
- Prosječne performanse ostaju iznad 55 FPS.
- Pet potpunih sesija prolazi bez neobrađene iznimke.

## 6. Otvorene stavke

- Završno paketiranje 2. srpnja 2026. prošlo je kroz `PATH=.venv/bin:$PATH ./scripts/package.sh`.
- Izrađen je `dist/Aetherfront-Zeppelin-Wars-macOS.zip` veličine približno 29 MB.
- ZIP je raspakiran u čistu privremenu mapu i potvrđeno je da sadrži izvršnu
  `Aetherfront.app` aplikaciju, `balance.json`, menu glazbu i cloud texture asset.
- Raspakirani executable pokrenut je s dummy SDL video/audio driverima i nije završio
  greškom tijekom kratkog smoke testa.
- Završni PDF dokumenti izvezeni su za projektni plan, GDD, tehničku dokumentaciju,
  izvještaj o testiranju i changelog.
- Prezentacija se izrađuje naknadno prema korisnikovoj odluci i nije dio ovog commita.
