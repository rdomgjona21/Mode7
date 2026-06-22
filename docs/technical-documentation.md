# Tehnička dokumentacija — Aetherfront: Zeppelin Wars

**Verzija:** 0.6

**Datum:** 22. lipnja 2026.

**Status:** Mode7 prototip, igračev prikaz i rani macOS paket

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

## Billboard projekcija

`WorldBillboard` povezuje PyGame površinu s položajem i širinom u koordinatama svijeta.
`BillboardProjector` najprije računa najkraći pomak kroz omotani svijet, a zatim ga
rastavlja na dubinu ispred kamere i bočni odmak. Objekti iza kamere, izvan najveće
udaljenosti ili potpuno izvan zaslona ne crtaju se.

Vidljivi objekt dobiva `pygame.Rect` čija veličina pada s dubinom. Donji rub pravokutnika
prati projekciju ravnine, pa objekt ostaje usidren u svijetu. `project_all()` sortira
rezultate od najudaljenijeg prema najbližem kako bi bliži objekti pravilno prekrili
udaljene. Sustav je pripremljen za buduće protivnike, projektile i popravke.

## Proceduralni Kestrel

`create_kestrel_surface()` crta transparentnu sliku 96×64 pomoću PyGame elipsi, poligona,
linija i krugova. Brod koristi mjedenu, tamnoželjeznu i cijan paletu te oblikom razlikuje
balon, trup, kabinu, peraje i pogon. Budući da kamera predstavlja položaj igrača u svijetu,
Kestrel ostaje vezan uz zaslon, vodoravno centriran i s donjim rubom na retku 344.

Prikaz je generiran kodom, pa nije dodan vanjski resurs ni zapis u licencne manifeste.

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
./scripts/package.sh
open dist/Aetherfront.app
```

Neobvezni argument `Game.run(max_frames=...)` postoji samo za ograničeno izvođenje u
automatiziranim testovima. U normalnom pokretanju aplikacija radi do zatvaranja prozora.

`package.sh` prvo izvodi Ruff i Pytest, zatim gradi prozorsku aplikaciju s identifikatorom
`hr.foi.aetherfront`. PyInstallerova konfiguracija i cache usmjereni su u ignoriranu mapu
`tmp/`, a skripta završava pogreškom ako izvršna datoteka unutar `.app` paketa ne postoji.
Rani ARM64 paket 22. lipnja uspješno je izgrađen, ostao aktivan u headless smoke testu i
stvarno se otvorio i zatvorio u macOS-u.

## Sljedeći tehnički korak

Sljedeća zasebna cjelina je osnova borbe: projektili, kružni sudari, šteta, zdravlje igrača,
kratka neranjivost i početna konfiguracija vrijednosti u `balance.json`.
