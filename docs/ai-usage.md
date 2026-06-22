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
