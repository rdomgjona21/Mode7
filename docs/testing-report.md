# Izvještaj o testiranju — Aetherfront: Zeppelin Wars

**Status:** prvi završni balance pass implementiran, ručni playtestovi još prazni  
**Datum početka:** 24. lipnja 2026.

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

## 3. Performanse

Izolirano mjerenje renderera pokreće se naredbom:

```bash
python scripts/benchmark_mode7.py --duration 12 --minimum 55
```

Prag prihvata ostaje najmanje 55 FPS. Završno mjerenje potrebno je ponoviti nakon
balansiranja i prije izrade release ZIP-a.

## 4. Ručni playtestovi

Za svaku potpunu sesiju treba ispuniti `tests/playtest-notes.md`. U izvještaj se zatim
prepisuju sažeci najvažnijih rezultata: trajanje, ishod, score, skupljeni repair pickupovi,
primljena šteta, dojam težine i pronađeni problemi.

| # | Datum | Commit | Ishod | Vrijeme | Score | Damage | Repairs | Napomena |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 |  |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |

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

- Ručno provjeriti prvi balance pass i po potrebi fino podesiti valove, oružja,
  survivability i bossa.
- Popuniti pet ručnih playtest zapisa.
- Ponoviti paketiranje i čisti ZIP smoke test.
