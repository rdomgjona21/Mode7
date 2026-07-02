# Projektni plan — Aetherfront: Zeppelin Wars

**Verzija:** 1.1

**Autor:** Robert Domgjonaj

**Oznaka projekta:** P5 — Mode7 / pucačina

**Planirano razdoblje:** 18. lipnja – 2. srpnja 2026.

**Opterećenje:** približno 28 sati tjedno; ukupno 66 sati

**Platforma:** macOS aplikacija za preuzimanje

**Tehnologije:** Python 3.12, PyGame, NumPy, PyInstaller

**Žanr i tema:** steampunk pucačina; rat zračnih brodova iznad industrijskih nebeskih otoka

> Administrativni uvjet ispunjen: nastavnik je 22. lipnja 2026. odobrio temu P5 i
> izmijenjeni individualni raspored.

## 1. Svrha i glavni cilj

Cilj je izraditi stabilnu, samostalnu macOS igru na engleskom jeziku pod nazivom **Aetherfront: Zeppelin Wars**. Igrač upravlja borbenim zračnim brodom u cjelovitoj misiji trajanja 10–15 minuta, poražava tri vala protivnika i uništava dreadnought s dvije faze. Projekt demonstrira učinkovit, NumPyjem vektoriziran Mode7 prikaz u PyGameu.

## 2. Mjerljivi posebni ciljevi

1. Izraditi jednu dovršenu razinu „Siege of Brasshaven” s tokom od glavnog izbornika do pobjede.
2. Održati prosječno najmanje 55 FPS pri najvećem predviđenom borbenom opterećenju na ciljanom M1 MacBook Airu.
3. Implementirati tri oružja, tri vrste protivnika, tri vala, predmete za popravak, bodovanje i šefa s dvije faze.
4. Uključiti upute, pauzu, poraz, pobjedu, HUD, zvuk, glazbu, čestice i jasnu povratnu informaciju sudara bez agresivnog podrhtavanja zaslona.
5. Proći automatizirane provjere prikaza, sudara, oružja, valova i licenci resursa.
6. Završiti pet uzastopnih ručnih igranja bez neobrađene iznimke.
7. Predati izvorni kod, macOS ZIP, projektni plan, GDD, tehničku dokumentaciju, izvještaj o testiranju, evidenciju resursa i izjavu o uporabi AI-ja; prezentacija se izrađuje naknadno prema korisnikovoj odluci.

## 3. Opseg

### Uključeno

- Jedna razina trajanja 10–15 minuta i jedan šef.
- Vektorizirana Mode7 ravnina i 2D objekti skalirani prema udaljenosti.
- Zračni brod s topom, raspršenom paljbom i raketama.
- Protivnici scout, gunship i bomber te tri skriptirana vala.
- Zdravlje, popravci, bodovi, vremena hlađenja, sudari i povratne informacije.
- Glavni izbornik, upute, pauza, poraz, pobjeda, HUD i zvuk.
- macOS `.app` i ZIP, dokumentacija, testovi i naknadna prezentacija.

### Isključeno

Višeigrački način, proceduralno stvaranje razina, više razina, spremanje, mrežna ljestvica, preglednička ili mobilna inačica, kontroler, uređivač razina, dodatni šefovi i razine težine nisu dio opsega.

## 4. Radni paketi i isporuke

| RP | Radni paket | Rezultat | Dokaz prihvata | Sati |
|---|---|---|---|---:|
| 1 | Planiranje i postavljanje | Repozitorij, okruženje, plan, početni GDD | Pokretanje izvornog koda | 8 |
| 2 | Prototip prikaza | Mode7, kamera, nebo, omatanje svijeta | Test ≥55 FPS | 12 |
| 3 | Borbeni sustavi | Oružja, projektili, šteta, popravci, sudari | Automatizirani testovi | 10 |
| 4 | Sadržaj i napredovanje | Tri vrste protivnika, tri vala, dvije faze šefa | Cjelovito igranje do pobjede | 12 |
| 5 | Sučelje i dorada | HUD, izbornici, zvuk, čestice, povratne informacije | Popis funkcionalnosti | 8 |
| 6 | Testiranje i balans | Pet igranja, popravci i balansiranje | Dnevnik testiranja | 8 |
| 7 | Izdanje i dokumentacija | `.app`, ZIP, PDF-ovi, licence, AI evidencija; PPTX naknadno | Provjera čistog izdanja | 8 |
| | **Ukupno** | | | **66** |

## 5. Trotjedni raspored

### Ganttov prikaz

| Aktivnost | 18.–20. 6. | 21.–23. 6. | 24.–26. 6. | 27.–29. 6. | 30. 6.–1. 7. | 2. 7. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Odobrenje zaprimljeno, plan i repozitorij | ███ | | | | | |
| Mode7 prikaz i kamera | ███ | ███ | | | | |
| Test performansi i rana aplikacija | | ███ | | | | |
| Borbeni sustavi | | | ███ | | | |
| Protivnici, valovi i šef | | | █ | ███ | | |
| Sučelje, zvuk i efekti | | | | ███ | | |
| Zamrzavanje funkcionalnosti i testovi | | | | | ███ | █ |
| Dokumentacija i prezentacija | █ | | █ | █ | ███ | █ |
| Provjera izdanja | | | | | ███ | █ |

### Ključne točke

- **21. lipnja — tehnički prag:** Mode7 stabilno radi na ≥55 FPS.
- **27. lipnja — igrivi borbeni tok:** moguće je odigrati cijelu borbu do pobjede nad šefom.
- **29. lipnja — zamrzavanje funkcionalnosti:** nastavljaju se samo popravci, balans, dokumentacija i izdanje.
- **2. srpnja — kandidat za izdanje:** dovršeni su izvorni kod, ZIP, PDF-ovi i dokazi; prezentacija se izrađuje naknadno.

## 6. Uloge i odgovornosti

Projekt je individualan. Robert Domgjonaj obavlja uloge voditelja projekta, programera, dizajnera igre, vizualnog dizajnera, integratora zvuka, testera i autora dokumentacije. Voditelj čuva opseg i raspored; programer izrađuje prikaz, mehanike i pakiranje; dizajner određuje petlju i balans; tester vodi automatizirane i ručne provjere; autor dokumentacije održava sve isporuke i licence.

## 7. Strategija kvalitete i testiranja

Svaka promjena mora proći `ruff check .` i `pytest`. Test Mode7 performansi obvezni je prag izdanja. Automatizirani testovi provjeravaju konačne i omotane projekcije, determinističke sudare, vrijeme hlađenja i štetu oružja, redoslijed valova, potpunost popisa resursa i osnovni tok aplikacije. Ručno se provjeravaju cijela igra, zapakirana aplikacija, kontrole, povratne informacije, sav sadržaj, pet cjelovitih igranja i pokretanje iz čistog ZIP-a.

## 8. Registar rizika

| Rizik | Vjerojatnost | Utjecaj | Mjera ublažavanja |
|---|---|---|---|
| Mode7 je prespor | Srednja | Visok | NumPy vektorizacija, 640×360, predizračuni i prag u prvom tjednu |
| Širenje opsega | Srednja | Visok | Fiksna ograničenja jedne razine, tri oružja, tri protivnika i jednog šefa |
| Kasna izrada šefa | Srednja | Srednji | Prvo ponašanje uz proceduralnu grafiku, zatim dorada |
| Neuspjelo pakiranje | Srednja | Visok | Rana izrada u prvom tjednu i ponavljanje nakon zamrzavanja |
| Kašnjenje resursa ili licenci | Niska | Srednji | Generirani resursi; odbacivanje svega bez jasne licence |
| Premalo vremena za testiranje | Srednja | Visok | Zamrzavanje 29. lipnja i završna tri dana bez novih funkcionalnosti |
| Neusklađena uporaba AI-ja | Niska | Visok | FOI razina 4, evidencija, provjera i zabrana povjerljivih podataka |
| Nema odobrenja nastavnika | Zatvoren 22. 6. | Visok | Odobrenje teme P5 i izmijenjenog rasporeda zaprimljeno je |

## 9. Izvještavanje o napretku

Napredak se tjedno zapisuje u dnevnik promjena. Izvještaj navodi završene radne pakete, planirane i stvarne sate, rezultate testova i performansi, aktivne rizike, odluke te plan za sljedećih sedam dana. Git povijest služi kao evidencija promjena, a kontrolni popis i bilješke testiranja kao dokaz prihvata.

## 10. Ograničenja, proračun i promjene

Novčani proračun iznosi 0 €. Koriste se alati otvorenog koda i vlastiti generirani resursi. Izvođenje ne ovisi o internetu. Svaka promjena opsega mora navesti trošak u satima i ukloniti barem jednako velik postojeći zahtjev. Nakon 29. lipnja nisu dopuštene nove funkcionalnosti. Potrebno odobrenje zaprimljeno je 22. lipnja 2026.; aplikacija, ZIP, PDF dokumentacija, licence i testni dokazi završeni su 2. srpnja 2026., a objava na itch.io i službena predaja slijede nakon naknadne prezentacije i završne korisničke odluke.
