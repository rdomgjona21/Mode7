# Evidencija uporabe generativne umjetne inteligencije

## 19. lipnja 2026. — aplikacijska osnova

- **Alat:** OpenAI Codex.
- **Namjena:** planiranje i izrada PyGame aplikacijske petlje, konfiguracije, osnovnih
  testova, validacijske skripte i početne tehničke dokumentacije.
- **Utjecaj:** Codex je predložio i implementirao početni kod koji autor mora pregledati,
  pokrenuti i razumjeti prije predaje.
- **Provjera:** Ruff, Pytest, headless pokretanje jednog framea i ručno pokretanje prozora.
- **Podaci:** nisu korištene vjerodajnice, osobni podaci ni povjerljivi sadržaj.

## 19. lipnja 2026. — obrazovna objašnjenja koda

- **Alat:** OpenAI Codex.
- **Namjena:** dodavanje hrvatskih komentara, docstringova i vodiča kroz postojeći kod.
- **Utjecaj:** ponašanje aplikacije nije mijenjano; dodana su samo objašnjenja namijenjena
  autorovu učenju i provjeri razumijevanja.
- **Provjera:** Ruff i Pytest nakon dokumentacijskih izmjena.

## 19. lipnja 2026. — upravljiva kamera

- **Alat:** OpenAI Codex.
- **Namjena:** implementacija modela kamere, vremenski neovisnog kretanja, obrade tipki,
  dijagnostičkog prikaza, testova i prateće dokumentacije.
- **Utjecaj:** dodana je tehnička osnova kretanja bez Mode7 prikaza i gameplaya.
- **Provjera:** Ruff, Pytest, testovi matematike kamere i pokretanje stvarnog prozora.

## 19. lipnja 2026. — operativni plan do 2. srpnja

- **Alat:** OpenAI Codex.
- **Namjena:** izrada i trajno spremanje dnevnog rasporeda završetka aplikacije i svih
  materijala do 2. srpnja 2026.
- **Utjecaj:** plan raspoređuje preostale funkcionalnosti, testiranje, dokumentaciju i
  izdanje na 13 dnevnih cjelina; ne mijenja ponašanje aplikacije.

## 19. lipnja 2026. — Mode7 projekcijska matematika

- **Alat:** OpenAI Codex.
- **Namjena:** implementacija vektoriziranog izračuna udaljenosti redaka, bočnih otklona,
  transformacije prema kameri, omatanja svijeta i automatiziranih testova.
- **Utjecaj:** dodane su matrice koordinata za buduće uzorkovanje Mode7 teksture; vizualni
  prikaz i gameplay nisu dodani.
- **Provjera:** Ruff, Pytest te testovi oblika, konačnosti, rotacije i omatanja projekcije.

## 19. lipnja 2026. — proceduralna tekstura terena

- **Alat:** OpenAI Codex.
- **Namjena:** implementacija determinističkog NumPy generatora industrijske teksture,
  validacije ulaza, testova i obrazovnih objašnjenja.
- **Utjecaj:** dodana je tekstura koja se stvara u memoriji bez vanjskih resursa; još nije
  povezana s vizualnim rendererom.
- **Provjera:** Ruff, Pytest te testovi oblika, tipa, raspona, seeda i raznolikosti boja.

## 20. lipnja 2026. — vizualni Mode7 renderer

- **Alat:** OpenAI Codex.
- **Namjena:** povezivanje projekcijskih koordinata i proceduralne teksture, izrada neba,
  horizonta, dijagnostičkog prikaza, benchmarka, testova i prateće dokumentacije.
- **Utjecaj:** tehnički prototip sada vizualno prikazuje ravninu koja se pomiče i rotira s
  kamerom; gameplay, igrač i drugi objekti nisu dodani.
- **Provjera:** Ruff, Pytest, headless frame te kratko i 60-sekundno mjerenje renderera.
- **Podaci:** nisu korištene vjerodajnice, osobni podaci ni povjerljivi sadržaj.

## 22. lipnja 2026. — billboardi, Kestrel i rani macOS paket

- **Alat:** OpenAI Codex.
- **Namjena:** implementacija perspektivne projekcije 2D objekata, proceduralnog prikaza
  igračeva broda, testova, PyInstaller skripte i prateće dokumentacije.
- **Utjecaj:** Kestrel je prvi vidljivi brod, generički sustav priprema prikaz budućih
  protivnika, a projekt se može izgraditi kao rana ARM64 macOS aplikacija.
- **Provjera:** Ruff, 49 Pytest testova, višeframesko headless izvođenje, pregled
  generiranog framea, PyInstaller build, provjera Mach-O datoteke i stvarno pokretanje i
  zatvaranje `.app` aplikacije.
- **Resursi:** brod je generiran kodom; nisu korištene vanjske slike ni zvukovi i zato
  licencni manifesti nisu mijenjani.
- **Podaci:** nisu korištene vjerodajnice, osobni podaci ni povjerljivi sadržaj.

## 22. lipnja 2026. — osnova borbe i sudara

- **Alat:** OpenAI Codex.
- **Namjena:** implementacija konfiguracije balansa, modela projektila, kružnih sudara,
  zdravlja, liječenja, privremene neranjivosti, testova i dokumentacije.
- **Utjecaj:** dodana je deterministička borbena jezgra koja još nije povezana s vidljivim
  pucanjem, protivnicima ni glavnom aplikacijskom petljom.
- **Provjera:** Ruff, 73 Pytest testa, 120-frame headless izvođenje, provjera prisutnosti
  `balance.json` u paketu te trosekundni smoke test ARM64 aplikacije.
- **Resursi:** nisu dodane slike, zvukovi ni drugi vanjski resursi.
- **Podaci:** nisu korištene vjerodajnice, osobni podaci ni povjerljivi sadržaj.

## 22. lipnja 2026. — evidencija odobrenja nastavnika

- **Alat:** OpenAI Codex.
- **Namjena:** usklađivanje projektnih dokumenata s informacijom autora da je nastavnik
  odobrio temu P5 i izmijenjeni individualni raspored.
- **Utjecaj:** administrativni uvjet i pripadajući rizik označeni su ispunjenima; opseg,
  rok i ponašanje aplikacije nisu mijenjani.
- **Provjera:** pretražene su sve reference na odobrenje i pokrenuti su Ruff i Pytest.
- **Podaci:** nije pohranjena poruka nastavnika ni drugi osobni ili povjerljivi sadržaj.

## 22. lipnja 2026. — oružja, pickup i osnovni HUD

- **Alat:** OpenAI Codex.
- **Namjena:** povezivanje cannona, spread guna i raketa s glavnom petljom, izrada
  trening-cilja, repair pickupa, proceduralnih prikaza, HUD-a, testova i dokumentacije.
- **Utjecaj:** prototip je prvi put ručno igriv kao borbena proba; privremeni cilj nije
  nova vrsta protivnika i bit će zamijenjen sadržajem iz zaključanog opsega.
- **Dodatna izmjena:** benchmark prikazuje napredak svakih deset sekundi i nakon `Ctrl+C`
  završava bez tracebacka.
- **Provjera:** Ruff, 86 Pytest testova, 120-frame headless izvođenje, pregled generiranog
  borbenog framea, kratki benchmark i PyInstaller smoke build.
- **Resursi:** svi novi prikazi generirani su PyGame kodom; nisu dodani vanjski resursi.
- **Podaci:** nisu korištene vjerodajnice, osobni podaci ni povjerljivi sadržaj.

## 23. lipnja 2026. — standardni protivnici

- **Alat:** OpenAI Codex.
- **Namjena:** implementacija scouta, gunshipa i bombera, njihovih vrijednosti balansa,
  kretanja, napada, proceduralnih prikaza, bodovanja, štete nad igračem, HUD izmjena,
  testova i prateće dokumentacije.
- **Utjecaj:** privremeni trening-cilj uklonjen je iz aktivnog gameplay toka; prototip
  sada koristi samo tri standardne vrste protivnika iz zaključanog opsega.
- **Provjera:** Ruff i 95 Pytest testova kroz `./scripts/validate.sh`, 120-frame headless
  pokretanje te 12-sekundni benchmark od 157,8 FPS-a uz prag 55 FPS-a.
- **Resursi:** svi novi prikazi generirani su PyGame kodom; nisu dodani vanjski resursi.
- **Podaci:** nisu korištene vjerodajnice, osobni podaci ni povjerljivi sadržaj.

## 23. lipnja 2026. — konfigurirani borbeni valovi

- **Alat:** OpenAI Codex.
- **Namjena:** implementacija `waves.json`, `WaveDirector`, povezivanja valova s
  `CombatSession`, prikaza vala u HUD-u, testova i prateće dokumentacije.
- **Utjecaj:** protivnici se više ne stvaraju kao beskonačna razvojna skupina, nego kroz
  tri konfigurirana redovna vala. Boss borba nije dodana u ovom koraku.
- **Provjera:** Ruff i 102 Pytest testa kroz `./scripts/validate.sh`, 180-frame headless
  pokretanje, 12-sekundni benchmark od 164,3 FPS-a uz prag 55 FPS-a te PyInstaller
  package build s provjerom `balance.json` i `waves.json`.
- **Resursi:** nije dodan vanjski sadržaj; `waves.json` je autorska konfiguracijska
  datoteka projekta.
- **Podaci:** nisu korištene vjerodajnice, osobni podaci ni povjerljivi sadržaj.

## 23. lipnja 2026. — prvi dio boss borbe

- **Alat:** OpenAI Codex.
- **Namjena:** implementacija ISS Goliath boss modela, boss balansa, proceduralnog prikaza,
  spawnanja nakon trećeg vala, dvije faze, burst paljbe, boss HUD-a, testova i prateće
  dokumentacije.
- **Utjecaj:** nakon čišćenja tri vala pojavljuje se rani boss susret. Boss prima štetu i
  prelazi u drugu fazu, ali score za uništenje, victory i game-over tok ostaju za sljedeći
  commit.
- **Provjera:** Ruff i 108 Pytest testova kroz `./scripts/validate.sh`, 180-frame headless
  pokretanje, 12-sekundni benchmark od 163,6 FPS-a uz prag 55 FPS-a te PyInstaller
  package build.
- **Resursi:** boss prikaz generiran je PyGame kodom; nisu dodani vanjski resursi.
- **Podaci:** nisu korištene vjerodajnice, osobni podaci ni povjerljivi sadržaj.

## 23. lipnja 2026. — završetak borbenog toka

- **Alat:** OpenAI Codex.
- **Namjena:** povezivanje uništenja bossa sa scoreom i pobjedom, povezivanje smrti igrača
  s game-over stanjem, zaustavljanje simulacije nakon terminalnog stanja, testovi i sažetak
  trenutačnog koda.
- **Utjecaj:** borbeni tok sada može završiti pobjedom nakon ISS Goliatha ili porazom nakon
  gubitka trupa. Glavni izbornik, restart i pauza nisu dodani u ovom koraku.
- **Provjera:** Ruff i 111 Pytest testova kroz `./scripts/validate.sh`, 180-frame headless
  pokretanje, 12-sekundni benchmark od 162,1 FPS-a uz prag 55 FPS-a te PyInstaller
  package build.
- **Resursi:** nisu dodani vanjski resursi.
- **Podaci:** nisu korištene vjerodajnice, osobni podaci ni povjerljivi sadržaj.
