# Tehnička dokumentacija — Aetherfront: Zeppelin Wars

**Verzija:** 0.2

**Datum:** 19. lipnja 2026.

**Status:** aplikacijska osnova i upravljiva kamera

## Arhitektura

Paket `aetherfront` koristi Python 3.12 i PyGame. Ulazna točka `python -m aetherfront`
stvara objekt `Game`, koji upravlja inicijalizacijom PyGamea, prozorom, glavnom petljom,
crtanjem i sigurnim gašenjem.

Prikaz se crta na internu površinu veličine 640×360 i skalira na prozor veličine
1280×720. Petlja je ograničena na 60 slika u sekundi. Trenutačna verzija prikazuje samo
tehnički prototip s dijagnostičkim prikazom kamere; Mode7 prikaz i gameplay još nisu
implementirani.

## Kamera i vrijeme

`Camera` čuva položaj `(x, y)`, smjer u radijanima i brzinu. Svaki frame prima proteklo
vrijeme `dt`, rotaciju i gas. Smjer se normalizira na jedan puni krug, brzina se ograničava
na 20–92 jedinice u sekundi, a položaj se omata unutar svijeta veličine 2.048 jedinica.

Tipke `A/D` ili lijevo/desno daju os rotacije, a `W/S` ili gore/dolje daju os gasa.
Kretanje koristi `dt`, zbog čega prijeđena udaljenost ne ovisi o broju frameova u sekundi.

## Pokretanje i provjera

```bash
source .venv/bin/activate
python -m aetherfront
./scripts/validate.sh
```

Neobvezni argument `Game.run(max_frames=...)` postoji samo za ograničeno izvođenje u
automatiziranim testovima. U normalnom pokretanju aplikacija radi do zatvaranja prozora.

## Sljedeći tehnički korak

Sljedeća zasebna cjelina je matematička osnova Mode7 projekcije. Vizualno uzorkovanje
teksture uvodi se tek nakon testova projekcijskih koordinata.
