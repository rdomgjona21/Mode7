# Tehnička dokumentacija — Aetherfront: Zeppelin Wars

**Verzija:** 0.1  
**Datum:** 19. lipnja 2026.  
**Status:** aplikacijska osnova

## Arhitektura

Paket `aetherfront` koristi Python 3.12 i PyGame. Ulazna točka `python -m aetherfront`
stvara objekt `Game`, koji upravlja inicijalizacijom PyGamea, prozorom, glavnom petljom,
crtanjem i sigurnim gašenjem.

Prikaz se crta na internu površinu veličine 640×360 i skalira na prozor veličine
1280×720. Petlja je ograničena na 60 slika u sekundi. Trenutačna verzija prikazuje samo
statični tehnički prototip; kamera, Mode7 prikaz i gameplay još nisu implementirani.

## Pokretanje i provjera

```bash
source .venv/bin/activate
python -m aetherfront
./scripts/validate.sh
```

Neobvezni argument `Game.run(max_frames=...)` postoji samo za ograničeno izvođenje u
automatiziranim testovima. U normalnom pokretanju aplikacija radi do zatvaranja prozora.

## Sljedeći tehnički korak

Sljedeća zasebna cjelina je kamera s položajem, smjerom i brzinom. Mode7 projekcija uvodi
se tek nakon što kamera i njezini izračuni budu zasebno testirani.
