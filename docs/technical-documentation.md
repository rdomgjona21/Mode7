# Tehnička dokumentacija — Aetherfront: Zeppelin Wars

**Verzija:** 0.8

**Datum:** 22. lipnja 2026.

**Status:** igriva Mode7 borbena proba i rani macOS paket

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

## Borbena osnova

`data/balance.json` trenutačno određuje 100 bodova zdravlja igrača, radijus sudara 18,
neranjivost od 0,75 sekundi te zadani radijus 4 i trajanje 3 sekunde za projektile.
`load_combat_balance()` učitava podatke paketnim putem i odbija nedostajuće objekte,
nebrojčane, beskonačne ili nepozitivne vrijednosti.

`Projectile` čuva položaj, smjer, brzinu, štetu, tim, radijus i preostalo trajanje.
Kretanje koristi `dt`, položaj se omata unutar svijeta, a istekli projektil prestaje biti
aktivan. `CircleBody` i `circles_overlap()` provjeravaju dodir kružnica najkraćim putem
preko granice svijeta.

`PlayerCombatState` počinje punim zdravljem, ograničava ga na raspon od nule do maksimuma
i nakon prihvaćene štete aktivira kratku neranjivost. Ponovljeni pogodak tijekom zaštite
se odbija, a liječenje vraća samo zdravlje koje nedostaje.

## Oružja, trening-cilj i pickup

`WeaponController` čuva odabrano primarno oružje te zasebna hlađenja za cannon, spread
gun i raketu. Cannon stvara jedan projektil, spread gun tri projektila pod kutovima
−0,16, 0 i +0,16 radijana, a raketa koristi neovisnu tipku i hlađenje. Aktivni broj
projektila ograničen je na 64.

`CombatSession` jednom po frameu povezuje ulaze, projektile, kružne sudare, zdravlje
trening-cilja, ponovno pojavljivanje, repair pickup i bodove. Cilj ima 100 HP i pojavljuje
se 400 jedinica ispred igrača. Nakon uništenja stvara popravak koji vraća do 24 HP-a,
dodaje 50 bodova i nestaje nakon 10 sekundi. Trening-cilj je razvojna pomoć, a ne četvrta
vrsta protivnika.

Proceduralne slike razlikuju mjedeni cannon, cijan spread gun, crvenu raketu, kružni cilj
i repair ćeliju. `BillboardProjector` ih zajednički sortira i crta. Engleski HUD prikazuje
trup, odabrano oružje, hlađenje rakete, bodove, cilj, brzinu i FPS.

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
`tmp/`, a skripta završava pogreškom ako izvršna datoteka ili paketni `balance.json`
unutar `.app` paketa ne postoje.
Rani ARM64 paket 22. lipnja uspješno je izgrađen, ostao aktivan u headless smoke testu i
stvarno se otvorio i zatvorio u macOS-u.

Mode7 benchmark sada tijekom 60-sekundnog izvođenja ispisuje napredak svakih 10 sekundi.
Prekid tipkama `Ctrl+C` vraća izlazni kod 130 i kratku poruku bez Python tracebacka.

## Sljedeći tehnički korak

Sljedeća zasebna cjelina zamjenjuje trening-cilj scoutom, gunshipom i bomberom te dodaje
njihovo kretanje, zdravlje, napade, proceduralne oblike i bodove.
