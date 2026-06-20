# Tehnička dokumentacija — Aetherfront: Zeppelin Wars

**Verzija:** 0.5

**Datum:** 20. lipnja 2026.

**Status:** vizualni Mode7 tehnički prototip

## Arhitektura

Paket `aetherfront` koristi Python 3.12 i PyGame. Ulazna točka `python -m aetherfront`
stvara objekt `Game`, koji upravlja inicijalizacijom PyGamea, prozorom, glavnom petljom,
crtanjem i sigurnim gašenjem.

Prikaz se crta na internu površinu veličine 640×360 i skalira na prozor veličine
1280×720. Petlja je ograničena na 60 slika u sekundi. Trenutačna verzija prikazuje
vizualni Mode7 prototip s dijagnostičkim podacima kamere i FPS-om; gameplay još nije
implementiran.

## Mode7 projekcija

`Mode7Projection` predizračunava perspektivu za 224 retka tla ispod horizonta na retku
135. Za redak zaslona `y` udaljenost uzorka računa se formulom:

`udaljenost = visina_kamere × žarišna_duljina / (y - horizont)`

Žarišna duljina proizlazi iz širine interne slike i horizontalnog vidnog polja od 60°.
Udaljenost se ograničava na 1.400 jedinica. Za svaki stupac zatim se računa bočni otklon,
a vektori kamere naprijed i desno pretvaraju udaljenost i otklon u koordinate svijeta.
Operator modulo omata obje koordinate unutar svijeta veličine 2.048 jedinica.

Rezultat `ProjectionGrid` sadrži `screen_rows`, `world_x` i `world_y`. Matrice koordinata
imaju oblik 224×640 i koristi ih `Mode7Renderer` za NumPy uzorkovanje teksture. U
izračunu nema Python petlje po pikselima.

## Proceduralna tekstura terena

`generate_terrain_texture(size=512, seed=7)` vraća kontinuiranu NumPy RGB matricu tipa
`uint8`. Periodične sinusne funkcije stvaraju olujno-plave zone, pragovi izdvajaju svjetlije
oblake i tamnije industrijske površine, a modularna mreža dodaje mjedene navigacijske
linije. Isti seed uvijek daje jednak rezultat, što olakšava ponovljive testove.

Tekstura se generira u memoriji tijekom pokretanja i ne koristi vanjske slike, autore ni
licence. Zbog toga nije potreban novi zapis u registru vanjskih resursa.

## Vizualni renderer

`Mode7Renderer` pretvara omotane koordinate svijeta u indekse proceduralne teksture.
Napredno NumPy indeksiranje uzorkuje sva 143.360 piksela tla odjednom, a
`pygame.surfarray.blit_array()` prenosi rezultat na internu površinu. Iznad tla crta se
unaprijed izračunata olujno-plava gradacija, a mjedena linija odvaja horizont.

Metoda `sample_ground()` odvojena je od crtanja kako bi se rezultat uzorkovanja mogao
automatizirano provjeriti. `draw()` prihvaća samo internu površinu 640×360, čime se
sprječava tiho rastezanje ili rezanje projekcije.

Na ciljanom M1 MacBook Airu izolirani 60-sekundni benchmark 20. lipnja 2026. izmjerio je
159,3 FPS-a, čime je tehnički prag od najmanje 55 FPS-a ostvaren za trenutačni renderer.
Mjerenje će se ponoviti pri najvećem planiranom borbenom opterećenju.

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
python scripts/benchmark_mode7.py --duration 60 --minimum 55
```

Neobvezni argument `Game.run(max_frames=...)` postoji samo za ograničeno izvođenje u
automatiziranim testovima. U normalnom pokretanju aplikacija radi do zatvaranja prozora.

## Sljedeći tehnički korak

Sljedeća zasebna cjelina je projekcija 2D objekata, dubinsko sortiranje, proceduralni
prikaz broda Kestrel i rana PyInstaller provjera macOS aplikacije.
