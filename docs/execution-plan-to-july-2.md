# Operativni plan završetka do 2. srpnja 2026.

**Status:** aktivni dnevni raspored  
**Razdoblje:** 20. lipnja – 2. srpnja 2026.  
**Planirano preostalo opterećenje:** 56 sati

Ovaj dokument čuva dogovoreni operativni raspored za potpuno završenu aplikaciju i sve
materijale do 2. srpnja. Formalni `project-plan.md` usklađen je s ovim rokom 19. lipnja.

## Evidencija napretka

- **19.6.:** Mode7 projekcijska matematika i testovi dovršeni su prije planiranog datuma.
- **19.6.:** proceduralni generator teksture terena dovršen je kao priprema za renderer.
- **20.6.:** implementirani su vizualno NumPy uzorkovanje, nebo, horizont i benchmark
  Mode7 renderera; 60-sekundno mjerenje ostvarilo je 159,3 FPS-a i prošlo prag od 55 FPS-a.
- **22.6.:** implementirani su projekcija i dubinsko sortiranje 2D objekata, proceduralni
  Kestrel te rani ARM64 `.app`; paket je izgrađen i uspješno pokrenut na macOS-u.
- **22.6.:** prije rasporeda dovršena je testirana borbena osnova: projektili, omotani
  kružni sudari, zdravlje, liječenje, neranjivost i paketna konfiguracija balansa.
- **22.6.:** zaprimljeno je odobrenje nastavnika za temu P5 i izmijenjeni individualni
  raspored; administrativni preduvjet je ispunjen.

## Dnevni raspored

| Datum | Sati | Posao | Rezultat i commit |
|---|---:|---|---|
| **20.6.** | 4 h | Zatražiti ili evidentirati odobrenje nastavnika. Uskladiti formalni projektni plan s rokom 2.7. Implementirati i testirati Mode7 projekcijsku matematiku: horizont, udaljenost redaka, koordinate svijeta i omatanje. | Konačne i omotane projekcijske koordinate. `Add Mode7 projection math` |
| **21.6.** | 5 h | Izraditi proceduralnu teksturu terena, NumPy uzorkovanje, nebo i horizont. Povezati prikaz s kamerom i provesti 60-sekundno mjerenje performansi. | Pokretljiv Mode7 prikaz s najmanje 55 FPS. `Render vectorized Mode7 terrain` |
| **22.6.** | 4 h | Implementirati projekciju 2D objekata, dubinsko sortiranje i skaliranje. Dodati proceduralni Kestrel i napraviti prvi PyInstaller `.app` smoke build. | Vidljiv igrač i provjerena rana aplikacija. `Add player billboard and macOS smoke build` |
| **23.6.** | 4 h | Dodati projektile, kružne sudare, štetu, zdravlje igrača i kratku neranjivost. Vrijednosti spremiti u `balance.json`. | Testirana osnova borbe. `Add combat and collision foundations` |
| **24.6.** | 4 h | Implementirati cannon, spread gun i rockets s hlađenjem. Dodati odabir oružja, popravke i osnovni HUD. | Tri oružja i pickup rade na testnim ciljevima. `Add weapons pickups and HUD` |
| **25.6.** | 5 h | Implementirati scout, gunship i bomber: kretanje, zdravlje, napade, proceduralne oblike i bodove. | Tri funkcionalne vrste protivnika. `Add standard enemy types` |
| **26.6.** | 4 h | Izraditi `waves.json` i `WaveDirector`. Implementirati tri vala, stanke, spawn položaje i završetak vala. Dodati kostur izvještaja o testiranju. | Moguće odigrati sva tri redovna vala. `Add configured combat waves` |
| **27.6.** | 5 h | Implementirati ISS Goliath s 900 HP, dvije faze, obrascima paljbe i scout pratnjom. Dodati boss HUD, pobjedu i poraz. | Cijeli borbeni tok do pobjede. `Add two-phase dreadnought boss` |
| **28.6.** | 4 h | Implementirati Main Menu, Instructions, Playing, Paused, Victory i Game Over, restart i povratak u izbornik. Početi prezentaciju i završni kontrolni popis. | Potpun tok od izbornika do završetka. `Complete application state flow` |
| **29.6.** | 4 h | Dodati sintetizirani zvuk, glazbenu podlogu, čestice, eksplozije, bljeskove i screen shake. Snimiti prve završne screenshotove. | Funkcionalno dovršena igra. `Add audio and combat feedback` |
| **30.6.** | 4 h | Zamrznuti funkcionalnosti. Balansirati borbu, profilirati opterećenje, odigrati tri potpune sesije i popraviti pronađene greške. | Stabilan release candidate i najmanje 55 FPS. `Balance and stabilize vertical slice` |
| **1.7.** | 5 h | Završiti hrvatske dokumente, PDF-ove, izvještaj o testiranju, licence, AI evidenciju i changelog. Završiti engleski PPTX, itch.io tekst i medije. Napraviti `.app` i ZIP. | Svi materijali i zapakirani kandidat. `Prepare release documentation and package` |
| **2.7.** | 4 h | Odigrati još dvije potpune sesije. Provjeriti čisti ZIP, kontrole, sadržaj, licence, jezike i prezentaciju. Popraviti samo blokirajuće greške i pokrenuti završne provjere. | Završena aplikacija i svi materijali. `Finalize Aetherfront release candidate` |

## Dnevni postupak

Svaki dan treba:

1. ažurirati hrvatsku tehničku dokumentaciju i AI evidenciju;
2. pokrenuti `./scripts/validate.sh`;
3. ručno provjeriti novu funkcionalnost;
4. zapisati stvarno potrošene sate i rezultate;
5. napraviti jedan commit i push izravno na `main`.

Sav tekst u igri i prezentaciji ostaje na engleskom. Dokumentacija, izvještaji i testni
obrasci ostaju na hrvatskom.

## Obvezni pragovi

- **21.6.:** Mode7 održava najmanje 55 FPS. Borbeni sustavi čekaju dok taj prag ne prođe.
- **27.6.:** moguće je odigrati cijelu borbu do pobjede nad šefom.
- **29.6.:** završava dodavanje funkcionalnosti.
- **30.6.:** tri potpune sesije završavaju bez neobrađene iznimke.
- **2.7.:** ukupno pet uspješnih sesija, čisti ZIP radi, a dokumentacija i prezentacija
  su završene.

Odobrenje nastavnika zaprimljeno je 22. lipnja 2026. Itch.io objava i službena predaja
provode se nakon dovršetka aplikacije, dokumentacije i završnih provjera.
