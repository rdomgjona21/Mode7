# Vodič kroz trenutačni kod

Ovaj dokument objašnjava aplikacijsku osnovu, kameru i vizualni Mode7 prototip prije
uvođenja gameplaya. Najlakše ih je razumjeti praćenjem redoslijeda kojim Python izvodi kod.

## 1. Pokretanje paketa

Naredba `python -m aetherfront` traži datoteku `aetherfront/__main__.py`. Ona uvozi
funkciju `main()` i poziva je. `raise SystemExit(main())` završava proces izlaznim kodom
koji vrati aplikacija; vrijednost `0` znači uspješan završetak.

`main.py` ne sadrži logiku crtanja. Njegov je jedini posao stvoriti `Game` i pokrenuti
metodu `run()`. Tako ulazna točka ostaje mala, a aplikacijska logika može se testirati
bez pokretanja naredbenog retka.

## 2. Konfiguracija

`config.py` sadrži vrijednosti koje koristi više dijelova aplikacije. `INTERNAL_SIZE` je
površina na koju se crta, dok je `WINDOW_SIZE` veličina prozora. Interna slika 640×360
povećava se točno dva puta na 1280×720. Boje su RGB trojke: crvena, zelena i plava
komponenta imaju vrijednosti od 0 do 255.

Odvajanje konfiguracije sprječava ponavljanje brojeva kroz kod. Buduća promjena naslova,
rezolucije ili FPS-a radi se na jednom mjestu.

## 3. Kamera i delta time

`Camera` je podatkovna klasa koja čuva položaj, smjer i brzinu. Metoda `update()` prima
`dt`, odnosno broj sekundi proteklih od prethodnog framea. Pomak je umnožak brzine i
vremena, pa računalo s više FPS-a ne pomiče kameru brže.

Smjer se zapisuje u radijanima. `cos(smjer)` daje vodoravni, a `sin(smjer)` okomiti dio
kretanja. Operator `% WORLD_SIZE` vraća položaj na suprotni rub kada prijeđe granicu
svijeta. Funkcija `_clamp()` ograničava ulaze na -1 do 1 i brzinu na vrijednosti iz GDD-a.

## 4. Mode7 projekcijska matematika

`Mode7Projection` ne crta sliku. Ona za svaki piksel tla odgovara na pitanje: „Koju
koordinatu svijeta ovaj piksel predstavlja?” Retci neposredno ispod horizonta predstavljaju
veliku udaljenost, a retci pri dnu zaslona predstavljaju prostor blizu kamere.

Konstruktor unaprijed računa udaljenosti redaka i bočne otklone stupaca jer se te vrijednosti
ne mijenjaju tijekom igre. Metoda `project(camera)` koristi `cos` i `sin` trenutnog smjera
kamere za vektore naprijed i desno te proizvodi dvije NumPy matrice: `world_x` i `world_y`.

Primjerice, središnji stupac nema bočni otklon. Ako je smjer kamere `0`, njegova vrijednost
`world_y` ostaje jednaka položaju kamere, dok `world_x` pokazuje dalje ispred nje. Nakon
rotacije za 90° isti stupac napreduje po osi `y`. Vizualni renderer koristi te koordinate
kao indekse proceduralne teksture.

## 5. Proceduralna tekstura terena

`generate_terrain_texture()` stvara cijelu sliku kao NumPy matricu umjesto spremanja PNG
datoteke. `np.meshgrid()` daje koordinate svih piksela odjednom, a nekoliko periodičnih
sinusnih i kosinusnih funkcija iz njih gradi osnovno polje. Seed određuje faze funkcija,
pa isti seed uvijek proizvodi jednaku teksturu.

Normalizirano polje pretvara se u RGB kanale. Maske zatim označavaju oblake, industrijske
zone i mjedene linije. Svaka maska istodobno mijenja mnogo piksela; ne postoji Python
petlja koja obrađuje jedan piksel po prolazu. Rezultat je matrica `uint8` istog formata
koji očekuje slikovni prikaz.

## 6. Vizualni Mode7 renderer

`Mode7Renderer.sample_ground()` množi koordinate svijeta omjerom veličine teksture i
svijeta. Tako nastaju indeksi piksela teksture. NumPy zatim jednom operacijom bira boju
za svaki piksel tla. Operator modulo zadržava indekse unutar teksture čak i pri prelasku
granice svijeta.

Metoda `draw()` prenosi unaprijed izračunatu gradaciju neba i uzorkovano tlo na PyGame
površinu. `np.swapaxes()` je potreban jer NumPy slike u ovom projektu koriste redoslijed
visina–širina, dok PyGameov `surfarray` očekuje širina–visina. Jedina obična linija koju
PyGame crta jest mjedeni horizont; ne postoji Python petlja po pikselima.

## 7. Billboardi i Kestrel

`WorldBillboard` opisuje gdje se 2D slika nalazi u svijetu. Projektor najprije primjenjuje
omatanje kako bi pronašao najkraći put između kamere i objekta. Skalarni produkt s
vektorom kamere daje dubinu, a skalarni produkt s desnim vektorom daje bočni odmak.
Negativna dubina znači da je objekt iza kamere.

Žarišna duljina pretvara bočni odmak u položaj na zaslonu. Ista dubina određuje veličinu
slike i položaj njezina donjeg ruba na ravnini. Nakon odbacivanja nevidljivih objekata
rezultati se sortiraju od najudaljenijeg prema najbližem i tek tada skaliraju i crtaju.

Kestrel nije svjetski billboard: kamera već predstavlja njegov položaj. Zato se njegova
proceduralno nacrtana transparentna površina postavlja na stalno mjesto pri dnu zaslona,
nakon terena i prije dijagnostičkog teksta.

## 8. Borbena osnova

`balance.json` odvaja brojčane vrijednosti od programskog koda. Učitavač pretvara njegove
dvije sekcije u nepromjenjive objekte `PlayerBalance` i `ProjectileBalance`. Time buduće
balansiranje ne zahtijeva traženje brojeva kroz više Python datoteka.

`Projectile.update()` računa pomak iz smjera, brzine i `dt`, omata položaj i smanjuje
trajanje. Svoj `CircleBody` izlaže sustavu sudara. Sudar računa najkraći pomak po svakoj
osi, kvadrira udaljenost i uspoređuje je s kvadratom zbroja radijusa, bez nepotrebnog
izračuna korijena.

`PlayerCombatState.take_damage()` vraća `True` samo kada je šteta stvarno prihvaćena.
Nakon toga `update()` odbrojava zaštitu. `heal()` vraća stvarno obnovljenu količinu, što
će kasnije omogućiti točan prikaz popravaka i spriječiti prelazak preko maksimuma.

## 9. Glavna petlja

`Game.run()` prvo provjerava testni argument `max_frames`, zatim inicijalizira PyGame.
Blok `try/finally` jamči poziv `pygame.quit()` čak i ako se tijekom izvođenja dogodi
iznimka.

Postoje dvije površine:

- `window` je stvarni prozor veličine 1280×720;
- `canvas` je interna slika veličine 640×360 na kojoj se crta sadržaj.

Petlja `while running` čini jedan frame u svakom prolazu:

1. čita događaje operacijskog sustava;
2. prekida rad nakon događaja `QUIT`;
3. pretvara pritisnute tipke u osi rotacije i gasa;
4. ažurira kameru pomoću `dt`;
5. crta Mode7 nebo, horizont i teren;
6. crta tekst i dijagnostičke vrijednosti na internu površinu;
7. povećava internu površinu na prozor;
8. prikazuje dovršenu sliku pozivom `pygame.display.flip()`.

`max_frames` se koristi samo u testovima kako bi se petlja sama zaustavila. U normalnom
pokretanju vrijednost je `None`, pa aplikacija radi dok korisnik ne zatvori prozor.

## 10. Automatizirani testovi

`test_config.py` provjerava da ključne postavke imaju očekivane vrijednosti.
`test_game.py` koristi SDL upravljačke programe `dummy`, zbog čega PyGame može izvesti
frame bez stvarnog prozora i zvučnog uređaja. Test zatim potvrđuje izlazni kod `0` i da
je PyGame uredno ugašen.

Drugi test šalje neispravnu vrijednost `max_frames=0` i očekuje `ValueError`. Testovi
kamere zasebno provjeravaju pomak, neovisnost o podjeli frameova, granice brzine,
normalizaciju smjera, omatanje svijeta i odbijanje negativnog vremena.

Testovi Mode7 projekcije provjeravaju oblike matrica, konačne vrijednosti, granice svijeta,
središnji smjer, rotaciju za 90°, omatanje i odbijanje neispravnih postavki.

Testovi generatora terena provjeravaju oblik, RGB raspon, determinističnost, promjenu
seeda, broj različitih boja i odbijanje neispravnih argumenata.

Testovi renderera provjeravaju oblik uzorkovanog tla, promjenu slike pri kretanju kamere,
popunjavanje neba, horizonta i tla te odbijanje pogrešnog formata teksture ili površine.

Testovi billboardskog sustava provjeravaju omatanje, odbacivanje objekata iza kamere,
skaliranje prema udaljenosti, rotaciju, dubinski redoslijed i crtanje. Testovi Kestrela
provjeravaju dimenzije, transparentnu pozadinu i prisutnost više vidljivih boja.

Testovi borbene osnove provjeravaju JSON vrijednosti i pogreške, obične i omotane sudare,
dodir kružnica, kretanje i istek projektila, zdravlje, smrt, liječenje te blokiranje
ponovljene štete tijekom neranjivosti.

## 11. Validacija

`scripts/validate.sh` pokreće dvije provjere. Ruff provjerava stil, uvoze i česte Python
pogreške. Pytest izvršava sve funkcije čiji naziv počinje s `test_`. Postavka
`set -euo pipefail` zaustavlja skriptu čim neka provjera ne uspije.

`scripts/benchmark_mode7.py` tijekom zadanog vremena neprekidno pomiče kameru i crta
Mode7 frameove bez ograničenja prozora. Izlazni kod je različit od nule ako prosjek padne
ispod zadanog praga, primjerice 55 FPS-a.

`scripts/package.sh` ponavlja validaciju i poziva PyInstaller za izradu ARM64 macOS
aplikacije. Rezultat u `dist/` nije dio Git repozitorija; skripta na kraju izričito
provjerava postoje li izvršna datoteka i `balance.json` unutar paketa.

Za učenje je korisno privremeno promijeniti jednu konstantu ili očekivanje u testu,
pokrenuti `./scripts/validate.sh`, pročitati pogrešku i zatim vratiti promjenu.
