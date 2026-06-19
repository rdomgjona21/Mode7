# Tehnička dokumentacija — Aetherfront: Zeppelin Wars

**Verzija:** 0.4

**Datum:** 19. lipnja 2026.

**Status:** aplikacijska osnova, kamera, Mode7 projekcija i generator terena

## Arhitektura

Paket `aetherfront` koristi Python 3.12 i PyGame. Ulazna točka `python -m aetherfront`
stvara objekt `Game`, koji upravlja inicijalizacijom PyGamea, prozorom, glavnom petljom,
crtanjem i sigurnim gašenjem.

Prikaz se crta na internu površinu veličine 640×360 i skalira na prozor veličine
1280×720. Petlja je ograničena na 60 slika u sekundi. Trenutačna verzija prikazuje samo
tehnički prototip s dijagnostičkim prikazom kamere; Mode7 prikaz i gameplay još nisu
implementirani.

## Mode7 projekcija

`Mode7Projection` predizračunava perspektivu za 224 retka tla ispod horizonta na retku
135. Za redak zaslona `y` udaljenost uzorka računa se formulom:

`udaljenost = visina_kamere × žarišna_duljina / (y - horizont)`

Žarišna duljina proizlazi iz širine interne slike i horizontalnog vidnog polja od 60°.
Udaljenost se ograničava na 1.400 jedinica. Za svaki stupac zatim se računa bočni otklon,
a vektori kamere naprijed i desno pretvaraju udaljenost i otklon u koordinate svijeta.
Operator modulo omata obje koordinate unutar svijeta veličine 2.048 jedinica.

Rezultat `ProjectionGrid` sadrži `screen_rows`, `world_x` i `world_y`. Matrice koordinata
imaju oblik 224×640 i spremne su za buduće NumPy uzorkovanje teksture. U izračunu nema
Python petlje po pikselima. Vizualni renderer još nije povezan s glavnom petljom.

## Proceduralna tekstura terena

`generate_terrain_texture(size=512, seed=7)` vraća kontinuiranu NumPy RGB matricu tipa
`uint8`. Periodične sinusne funkcije stvaraju olujno-plave zone, pragovi izdvajaju svjetlije
oblake i tamnije industrijske površine, a modularna mreža dodaje mjedene navigacijske
linije. Isti seed uvijek daje jednak rezultat, što olakšava ponovljive testove.

Tekstura se generira u memoriji tijekom pokretanja i ne koristi vanjske slike, autore ni
licence. Zbog toga u ovom koraku nije dodan novi asset zapis. Vizualni renderer još ne
uzorkuje teksturu; to je sljedeća zasebna cjelina.

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

Sljedeća zasebna cjelina je proceduralna tekstura i vizualno NumPy uzorkovanje pomoću
izračunatih koordinata, uz 60-sekundnu provjeru cilja od najmanje 55 FPS.
