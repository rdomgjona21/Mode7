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

## 5. Cloud tekstura terena

`load_terrain_texture()` prvo pokušava učitati projektni PNG asset
`cloud_layer.png`. PyGame ga čita kao sliku, a `pygame.surfarray.array3d()` pretvara ga u
NumPy matricu istog RGB formata koji koristi Mode7 renderer. Zato renderer ne mora znati
je li tekstura došla iz datoteke ili iz proceduralnog fallbacka.

Ako PNG ne postoji ili se ne može učitati, `load_terrain_texture()` koristi
`generate_terrain_texture()`. Taj fallback i dalje stvara cijelu sliku kao NumPy matricu:
`np.meshgrid()` daje koordinate svih piksela odjednom, a periodične sinusne funkcije i
maske stvaraju oblačni uzorak bez Python petlje po pojedinačnim pikselima.

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
nakon terena i prije dijagnostičkog teksta. Njegov prikaz sada koristi Victorian airship
detalje: platneni balon, drvenu gondolu, mjedene nosače, zakovice, kabinu, dimnjak i aether
pogon.

## 8. Borbena osnova

`balance.json` odvaja brojčane vrijednosti od programskog koda. Učitavač pretvara njegove
sekcije u nepromjenjive objekte za igrača, projektile, oružja, popravke i protivnike. Time
balansiranje ne zahtijeva traženje brojeva kroz više Python datoteka.

`Projectile.update()` računa pomak iz smjera, brzine i `dt`, omata položaj i smanjuje
trajanje. Svoj `CircleBody` izlaže sustavu sudara. Sudar računa najkraći pomak po svakoj
osi, kvadrira udaljenost i uspoređuje je s kvadratom zbroja radijusa, bez nepotrebnog
izračuna korijena.

`PlayerCombatState.take_damage()` vraća `True` samo kada je šteta stvarno prihvaćena.
Nakon toga `update()` odbrojava zaštitu. `heal()` vraća stvarno obnovljenu količinu, što
će kasnije omogućiti točan prikaz popravaka i spriječiti prelazak preko maksimuma.

## 9. Oružja, protivnici i borbena sesija

`WeaponController` nakon svakog framea smanjuje tri neovisna hlađenja. Primarna paljba
čita trenutačni odabir, dok raketa ima zasebnu metodu. Obje metode najprije provjeravaju
hlađenje i slobodna mjesta, pa tek zatim stvaraju konfigurirane projektile malo ispred
kamere.

`Enemy` opisuje scouta, gunship i bombera. Svaki protivnik ima vrstu, položaj, smjer,
zdravlje, brzinu, radijus sudara, bodove, kontaktnu štetu, projektil i hlađenje napada.
Metoda `update()` ga pomiče prema igraču kroz omotani svijet, a `fire_if_ready()` vraća
neprijateljski projektil samo kada je hlađenje završeno.

`WaveDirector` učitava `waves.json`, prati trenutačni val, odgode spawnova, stanke između
valova i završetak trećeg vala. Spawn položaji nisu apsolutne koordinate nego udaljenost
ispred kamere i bočni pomak, pa se svaki val pojavljuje u odnosu na smjer kojim igrač leti.

`DreadnoughtBoss` opisuje ISS Goliath nakon završetka valova. Boss ima vlastito zdravlje,
radijus sudara, dvije faze, cooldown i burst paljbu. Faza se ne sprema ručno, nego se
računa iz preostalog zdravlja: iznad 50 % je prva faza, a na 50 % ili manje počinje druga
faza s pet projektila i kraćim hlađenjem. `CombatSession` dodatno prati je li već dodijeljen
boss-critical repair; kada Goliath u drugoj fazi prvi put padne na 20 % zdravlja ili manje,
igrač dobiva 50 HP-a do maksimalnog dopuštenog zdravlja.

`CombatSession` je središte borbene probe. Ažurira `WaveDirector`, projektile, protivnike,
njihove napade, boss susret, sudare igrača i neprijatelja, nastanak popravaka i bodove.
Nakon `waves_complete` stvara Goliath ispred kamere. Kada je boss uništen, dodaje se
boss score i postavlja `victory`; kada igrač ostane bez trupa, postavlja se `game_over`.
Time glavna PyGame petlja ne mora sadržavati pravila štete, bodovanja, spawnova i isteka
objekata.

Za balansiranje sesija dodatno bilježi `elapsed_time`, `enemies_destroyed`,
`repairs_collected` i `damage_taken`. Ti brojači ne utječu na pravila igre, nego daju
konkretne podatke za ručni playtest: koliko je pokušaj trajao, koliko je protivnika
uništeno, koliko je popravaka skupljeno i koliko je štete igrač stvarno primio.

HUD samo čita stanje sesije. Ne mijenja zdravlje, hlađenja ni bodove, koristi gornju
horizontalnu steampunk traku, borbeni font od izbornika, prikazuje vrijeme pokušaja i
moguće ga je zasebno testirati crtanjem na običnu headless površinu.

## 10. Glavna petlja

`Game.run()` prvo provjerava testni argument `max_frames`, zatim inicijalizira PyGame.
Blok `try/finally` jamči poziv `pygame.quit()` čak i ako se tijekom izvođenja dogodi
iznimka.

Postoje dvije površine:

- `window` je stvarni prozor veličine 1280×720;
- `canvas` je interna slika veličine 640×360 na kojoj se crta sadržaj.

Petlja `while running` čini jedan frame u svakom prolazu:

1. čita događaje operacijskog sustava;
2. prekida rad nakon događaja `QUIT`;
3. mijenja `AppState` za izbornik, upute, igranje i pauzu;
4. resetira kameru i `CombatSession` kada se pokreće nova misija;
5. pretvara pritisnute tipke u osi rotacije i gasa;
6. obrađuje odabir oružja, paljbu i raketu samo tijekom igranja;
7. ažurira kameru i borbenu sesiju pomoću `dt` samo u aktivnom `PLAYING` stanju;
8. crta Mode7 teren i dubinski sortirane borbene objekte;
9. crta Kestrel, gornji horizontalni HUD i eventualni panel izbornika;
10. povećava internu površinu na prozor;
11. prikazuje dovršenu sliku pozivom `pygame.display.flip()`.

`AppState` se nalazi u `core/states.py`. To je mali `StrEnum` s vrijednostima
`MAIN_MENU`, `INSTRUCTIONS`, `PLAYING` i `PAUSED`. Terminalni ishod nije posebno
aplikacijsko stanje, nego ostaje u `CombatSession` kroz `victory` i `game_over`, jer je
izravno posljedica borbenih pravila.

`ui/menus.py` crta engleske panele preko scene. Glavni izbornik objašnjava cilj i tipke
za start, upute prikazuju kontrole, pauza nudi nastavak/restart/izbornik, a završni panel
prikazuje pobjedu ili poraz, konačni score i sljedeće akcije.

`max_frames` se koristi samo u testovima kako bi se petlja sama zaustavila. U normalnom
pokretanju vrijednost je `None`, pa aplikacija radi dok korisnik ne zatvori prozor.

## 11. Automatizirani testovi

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

Testovi parallax pripreme provjeravaju da slojevi odgovaraju području neba iznad horizonta,
da postoje tri imenovana sloja, da su deterministički za isti seed, da se mijenjaju s
drugim seedom, da imaju vidljive alfa piksele, suptilne alfa vrijednosti i različite
faktore budućeg pomaka.

Testovi renderera provjeravaju oblik uzorkovanog tla, promjenu slike pri kretanju kamere,
popunjavanje neba, horizonta i tla, promjenu parallax neba pri kretanju kamere, redoslijed
parallax offseta prema faktoru pomaka te odbijanje pogrešnog formata teksture ili površine.

Testovi billboardskog sustava provjeravaju omatanje, odbacivanje objekata iza kamere,
skaliranje prema udaljenosti, rotaciju, dubinski redoslijed i crtanje. Testovi Kestrela
provjeravaju dimenzije, transparentnu pozadinu i prisutnost više vidljivih boja.

Testovi borbene osnove provjeravaju JSON vrijednosti i pogreške, obične i omotane sudare,
dodir kružnica, kretanje i istek projektila, zdravlje, smrt, liječenje te blokiranje
ponovljene štete tijekom neranjivosti.

Testovi stanja i izbornika provjeravaju stabilne vrijednosti `AppState`, reset novog
pokušaja te da se svaki panel može nacrtati na headless površinu.

Testovi efekata provjeravaju lifetime, pauzirano ažuriranje, projekciju ovisnu o smjeru
kamere, headless crtanje damage markera, muzzle flasha i kombiniranog feedbacka.

Testovi oružja provjeravaju broj, kutove, štetu, hlađenja i ograničenje projektila.
Testovi protivnika provjeravaju zaključane razlike scouta, gunshipa i bombera, primanje
štete, determinističko kretanje i hlađenje neprijateljske paljbe. Testovi valova provjeravaju
učitavanje tri vala, redoslijed spawnova, odgode, prijelaz između valova i završetak trećeg
vala. Testovi bossa provjeravaju početno zdravlje, prijelaz u drugu fazu, širi burst i
uništenje. Testovi sesije provjeravaju prvi konfigurirani val, prijelaz na drugi val,
stvaranje bossa nakon trećeg vala, boss damage, bodove, nastanak i prikupljanje popravka,
victory, game-over stanje, terminalno zaustavljanje simulacije, ograničenje projektila i
štetu nad igračem, telemetry vrijeme, broj uništenih protivnika, broj skupljenih popravaka
i ukupno primljenu štetu. HUD i benchmark imaju zasebne headless testove, uključujući
provjeru da borbeni HUD ostaje u gornjoj horizontalnoj traci.

## 12. Validacija

`scripts/validate.sh` pokreće dvije provjere. Ruff provjerava stil, uvoze i česte Python
pogreške. Pytest izvršava sve funkcije čiji naziv počinje s `test_`. Postavka
`set -euo pipefail` zaustavlja skriptu čim neka provjera ne uspije.

`scripts/benchmark_mode7.py` tijekom zadanog vremena neprekidno pomiče kameru i crta
Mode7 frameove bez ograničenja prozora. Izlazni kod je različit od nule ako prosjek padne
ispod zadanog praga, primjerice 55 FPS-a. Svakih deset sekundi ispisuje napredak, uvijek
šalje završni progress signal, a `Ctrl+C` završava kratkom porukom bez tracebacka.

`scripts/package.sh` ponavlja validaciju i poziva PyInstaller za izradu ARM64 macOS
aplikacije. Rezultat u `dist/` nije dio Git repozitorija; skripta na kraju izričito
provjerava postoje li izvršna datoteka, `balance.json`, `waves.json` i osnovni SFX asset
unutar paketa.

Za učenje je korisno privremeno promijeniti jednu konstantu ili očekivanje u testu,
pokrenuti `./scripts/validate.sh`, pročitati pogrešku i zatim vratiti promjenu.

## 13. Sažetak trenutačnog sustava

Aplikacija se pokreće naredbom `python -m aetherfront`. `main.py` stvara `Game`, a
`Game.run()` upravlja PyGame prozorom, eventima, kamerom, borbenom sesijom i crtanjem.

Prikaz koristi internu sliku 640×360 skaliranu na 1280×720. `Mode7Projection` računa
omotane koordinate tla, `Mode7Renderer` ih NumPyjem uzorkuje iz proceduralne teksture, a
`BillboardProjector` crta svjetske objekte kao 2D spriteove skalirane po udaljenosti.
`parallax.py` stvara proceduralne slojeve neba, a `Mode7Renderer` ih blita iznad horizonta
sa stišanim alfa vrijednostima i sporijim horizontalnim pomakom od kretanja tla.

Kestrel je vezan uz donji dio ekrana, dok kamera predstavlja položaj i smjer igrača u
svijetu. `balance.json` sadrži vrijednosti zdravlja, oružja, protivnika, popravka i bossa.
`waves.json` sadrži tri vala i njihove spawn odgode.

Borbena petlja povezuje kretanje kamere, oružja, neprijatelje, valove, sudare, pickupove,
boss borbu, bodove, pobjedu i poraz. `CombatSession` drži većinu gameplay stanja i kratki
`CombatFeedback` zadnjeg framea te osnovni telemetry za balansiranje, dok `AppState` drži
tok izbornika, uputa, igranja i pauze. Kada se repair pickup stvarno pokupi, feedback nosi
njegovu svjetsku poziciju do `EffectsState`, koji crta kratki zeleni/cijan plus efekt, i
do `AudioManager`, koji reproducira odgovarajući ElevenLabs SFX. Zona skupljanja je
namjerno znatno veća od osnovnog sidrišnog radijusa pickupa kako bi se collect i zeleni
feedback aktivirali čim igrač uđe u područje velikog perspektivnog plusa. Renderer, HUD,
efekti, audio manager i menu paneli uglavnom samo čitaju podatke i prikazuju ih.

Trenutačno rade tri oružja, tri standardna protivnika, tri vala, repair pickup, score, ISS
Goliath s dvije faze, jednokratni hitni popravak na 20 % boss healtha u fazi 2, boss health
bar, glavni izbornik, upute, pauza, restart flow, suptilne eksplozije, repair flash, boss
spark, muzzle flash, damage marker, `VICTORY` i `GAME OVER`. Kestrel, protivnici, Goliath i repair ćelija imaju proceduralni Victorian
airship polish, industrijski sky sloj ima dodatne dimne plumeove, a HUD koristi gornju
horizontalnu minimalističku steampunk traku s mjedenim rubovima i segmentiranim barovima.
ElevenLabs SFX pokriva oružja, protivnike, bossa, repair, UI i terminalna stanja.
Generirana WAV glazba sada ima zasebne loopove za menu, tri vala i dvije boss faze, a `Game`
automatski mijenja temu prema trenutačnom valu ili boss fazi. Prvi završni balance pass je
primijenjen kroz `balance.json` i `waves.json`. Autor je 2. srpnja 2026. potvrdio pet i
više ručnih sesija bez neobrađene iznimke, završni hrvatski dokumenti izvezeni su u PDF,
a `./scripts/package.sh` izrađuje i provjerava release ZIP. Prezentacija se izrađuje
naknadno prema korisnikovoj odluci.
