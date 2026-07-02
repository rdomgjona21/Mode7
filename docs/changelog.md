# Changelog — Aetherfront: Zeppelin Wars

Ovaj dokument sažima glavne razvojne promjene projekta. Detaljna evidencija AI uporabe,
testiranja i dizajnerskih odluka nalazi se u `docs/ai-usage.md`, `docs/testing-report.md`
i `docs/gdd.md`.

## 2. srpnja 2026.

- Projekt označen kao release kandidat.
- Evidentirano je više od pet ručnih playtest sesija bez neobrađene iznimke.
- Dodan je završni kontrolni popis prihvata u `tests/acceptance-checklist.md`.
- Završna automatizirana provjera prolazi s 190 Pytest testova.
- Mode7 benchmark iznosi 159,9 FPS u 12-sekundnom mjerenju, iznad praga od 55 FPS.
- `scripts/package.sh` sada izrađuje `dist/Aetherfront.app` i
  `dist/Aetherfront-Zeppelin-Wars-macOS.zip`.
- ZIP se raspakirava u čistu privremenu mapu i provjerava da sadrži izvršnu aplikaciju.
- Raspakirana aplikacija prošla je kratki smoke test s dummy SDL video/audio driverima.
- Dodan je jednokratni boss-critical repair: u boss phase 2, kada ISS Goliath prvi put
  padne na 20 % healtha ili manje, igrač dobiva 50 HP-a do maksimalnog healtha.

## 1. srpnja 2026.

- Player health vraćen je na 100 HP.
- Mode7 podloga zamijenjena je generiranim fotorealističnim cloud PNG assetom.
- Renderer zadržava proceduralni cloud fallback ako PNG asset nije dostupan.
- Dodan je svjetliji atmosferski haze kako bi se podloga čitala kao let iznad oblaka.
- Paketiranje uključuje i provjerava cloud texture asset.

## 30. lipnja 2026.

- Refaktoriran je `Game.run()` u manje metode za događaje menija, igre i pauze.
- Dodani su state transition testovi.
- Zajednička validation logika izdvojena je za projektile, protivnike i bossa.
- Sinkroniziran je repair pickup SFX sa zelenim vizualnim feedbackom.
- Dodani su komentari u ključne dijelove audio i gameplay koda.

## 27. lipnja 2026.

- Integrirani su ElevenLabs SFX asseti za oružja, protivnike, bossa, UI, repair, pobjedu
  i game-over stanje.
- Dodani su generirani WAV glazbeni loopovi za menu, tri vala i dvije boss faze.
- Audio manager mijenja glazbu prema meniju, valu ili boss fazi.
- SFX volumeni su smanjeni kako bi glazba ostala čujna tijekom borbe.

## 25. lipnja 2026.

- Primijenjen je prvi završni balance pass.
- HUD je preoblikovan u gornju horizontalnu minimalističku steampunk traku.
- Balansirani su health, repair pickup, stanke između valova, rakete i izdržljivost bossa.

## 24. lipnja 2026.

- Dodan je zeleni/cijan visual feedback za repair pickup.
- Dodana je osnovna telemetry za balansiranje: vrijeme pokušaja, uništeni protivnici,
  skupljeni repair pickupovi i primljena šteta.
- Kestrel, standardni protivnici, Goliath i repair ćelija dobili su Victorian airship
  proceduralni polish.

## 23. lipnja 2026.

- Dodani su scout, gunship i bomber.
- Dodan je `waves.json` i `WaveDirector` s tri konfigurirana vala.
- Implementiran je ISS Goliath boss s dvije faze, boss HUD-om i pobjedom nakon uništenja.
- Dodan je game-over tok kada igrač izgubi trup.
- Implementirani su main menu, instructions, pause, restart i povratak u menu.
- Dodani su suptilni vizualni efekti: eksplozije, boss spark, muzzle flash i damage marker.
- Dodani su proceduralni parallax sky slojevi iznad horizonta.

## 22. lipnja 2026.

- Evidentirano je odobrenje nastavnika za temu P5 i izmijenjeni individualni raspored.
- Dodan je billboard sustav, proceduralni Kestrel i rani macOS smoke build.
- Dodani su projektili, kružni sudari, health, healing, invulnerability i `balance.json`.
- Dodana su tri oružja: cannon, spread gun i rockets.
- Dodan je repair pickup, bodovanje i osnovni HUD.

## 19.-20. lipnja 2026.

- Postavljena je PyGame aplikacijska osnova.
- Implementirana je kamera s rotacijom, brzinom i omatanjem svijeta.
- Implementirana je Mode7 projekcijska matematika.
- Dodan je vektorizirani NumPy Mode7 renderer s nebom, horizontom i terrain samplingom.
- Izolirani Mode7 benchmark potvrdio je prag iznad 55 FPS.

## 18. lipnja 2026.

- Definiran je projekt Aetherfront: Zeppelin Wars kao P5 Mode7 / shoot 'em up.
- Izrađen je početni projektni plan, GDD i struktura repozitorija.
- Zaključan je opseg: jedna razina, tri oružja, tri standardna protivnika i jedan boss s
  dvije faze.
