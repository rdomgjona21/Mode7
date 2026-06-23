# Dokument dizajna igre — Aetherfront: Zeppelin Wars

**Verzija:** 1.0  
**Autor:** Robert Domgjonaj  
**Datum:** 18. lipnja 2026.  
**Status:** početni nacrt; aplikacijski tok, suptilni vizualni feedback i parallax sky implementirani

## Sadržaj

1. Koncept
2. Publika, platforma i pristupačnost
3. Svijet i priča
4. Temeljna petlja i napredovanje
5. Kontrole i igrač
6. Oružja i nagrade
7. Protivnici, valovi i šef
8. Sučelje i stanja igre
9. Vizualni i zvučni smjer
10. Tehnička arhitektura
11. Specifikacija razine
12. Ciljevi balansa i prihvata
13. Razvoj i objava
14. Rizici, izvori, licence, AI, pojmovnik i promjene

## 1. Koncept

**Aetherfront: Zeppelin Wars** brza je steampunk pucačina u kojoj igrač upravlja zračnim brodom iznad beskrajnog industrijskog krajolika u oblacima. Vektorizirana Mode7 ravnina stvara osjećaj brzine i rotacije, a protivnici se prikazuju kao 2D objekti skalirani prema udaljenosti. Vertikalni presjek prikazuje obranu Brasshavena od imperijalnog dreadnoughta.

### Stupovi dizajna

1. **Zamah:** brod se neprestano kreće, pa upravljanje i brzina zahtijevaju predviđanje.
2. **Čitljiv pritisak:** prepoznatljivi oblici, projektili, HUD i ritam valova jasno komuniciraju prijetnje.
3. **Sažeti spektakl:** jedna dovršena misija raste od scoutova do šefa s više faza.
4. **Pouzdan rad bez mreže:** nisu potrebni račun, usluga, internet ni preuzimanje sadržaja.

### Posebnost

Projekt spaja retro Mode7 ravninu, zračne brodove kao 2D objekte, suvremeni široki format i steampunk resurse generirane kodom. Cijeli borbeni razvoj izveden je u maloj PyGame aplikaciji bez gotovih paketa grafike.

## 2. Publika, platforma i pristupačnost

Ciljana publika su igrači stariji od 12 godina koji vole arkadne pucačine i retro prikaz. Primarno izdanje je besplatna macOS aplikacija na itch.io, a sesija traje 10–15 minuta.

Pristupačnost uključuje zaslon s uputama, alternativne tipke za upravljanje i brzinu, projektile visokog kontrasta, stalno vidljive zdravlje, bodove i val, velike natpise, pauzu i brzo ponovno pokretanje. Boja je podržana oblikom i kretanjem, a zvuk nije jedini nositelj informacije. Sav tekst unutar igre je na engleskom.

## 3. Svijet i priča

Brasshaven je neovisni nebeski grad pogonjen aether turbinama. Imperijalna armada približava se iza dreadnoughta **ISS Goliath**. Igrač zapovijeda patrolnim brodom **Kestrel**, presreće pratnju, prikuplja ćelije za popravak i uništava dreadnought prije njegova dolaska do grada.

Priča se prenosi naslovima i kratkim upozorenjima kako bi fokus ostao na akciji. Pobjeda čuva neovisnost Brasshavena; poraz omogućuje trenutačni novi pokušaj.

## 4. Temeljna petlja i napredovanje

1. Pročitati cilj i kontrole.
2. Upravljati brodom i mijenjati brzinu radi poravnanja protivnika s prednjim lukom paljbe.
3. Odabrati top ili raspršenu paljbu te koristiti rakete protiv izdržljivih ciljeva.
4. Izbjegavati projektile i sudare te očistiti trenutačni val.
5. Prikupiti povremene popravke i povećavati bodove.
6. Poražavati tri sve zahtjevnija vala.
7. Poražavati dreadnought kroz dvije faze i napade pratnje.
8. Doći do pobjede, pregledati bodove te ponoviti igru ili se vratiti u izbornik.

Izazov raste kroz izdržljivost protivnika, miješane formacije, preklapanje paljbe i promjenu faze šefa. Nagrade su bodovi, popravci, snažna audiovizualna povratna informacija, napredak vala i završna pobjeda.

## 5. Kontrole i model igrača

| Radnja | Unos | Ponašanje |
|---|---|---|
| Rotacija | A/D ili lijevo/desno | 1,65 radijana u sekundi |
| Brzina | W/S ili gore/dolje | 20–92 jedinice svijeta u sekundi |
| Odabir oružja | 1 / 2 | Top / raspršena paljba |
| Primarna paljba | Space | Puca ako je hlađenje završeno |
| Raketa | lijevi/desni Shift | Neovisno vrijeme hlađenja |
| Pauza | Esc | Zaustavlja simulaciju i prikazuje izbornik |

Kestrel počinje s 500 bodova trupa i 1,5 sekundi neranjivosti nakon pogotka. Brod je vizualno pri dnu zaslona, dok kamera prati njegov položaj i smjer u svijetu.

## 6. Oružja i nagrade

| Oružje | Uloga | Šteta | Hlađenje | Ponašanje |
|---|---|---:|---:|---|
| Cannon | Precizna stalna paljba | 16 | 0,18 s | Jedan brz mjedeni projektil |
| Spread gun | Blizina i više ciljeva | 10 × 3 | 0,34 s | Tri cijan projektila pod ±0,16 rad |
| Rocket | Velika trenutna šteta | 48 | 1,15 s | Jedna sporija velika raketa |

Uništeni protivnici donose 120–420 bodova, a šef 5.000. Popravak vraća 24 boda trupa i daje 50 bodova te nestaje nakon ograničenog vremena.

## 7. Protivnici, valovi i šef

| Protivnik | Svrha | Trup | Brzina | Napad |
|---|---|---:|---:|---|
| Scout | Brzi pritisak i pratnja | 28 | 62 | Lagan hitac i bliska potjera |
| Gunship | Dvoboj srednjeg dometa | 62 | 40 | Redovita ciljana paljba |
| Bomber | Izdržljiv snažan cilj | 96 | 27 | Spor, težak projektil |

Prvi val uvodi šest scoutova. Drugi kombinira pet scoutova i tri gunshipa. Treći donosi pet scoutova, četiri gunshipa i dva bombera. Između očišćenih valova postoji kratka stanka.

**Imperial Dreadnought** ima 900 bodova trupa. U prvoj fazi puca u nizu od tri projektila. Na 50 % trupa započinje druga faza: interval paljbe pada s 0,78 na 0,42 sekunde, niz se širi na pet projektila, a periodično dolaze scoutovi. Velik oblik, zasebna traka zdravlja, upozorenje i završno podrhtavanje jasno komuniciraju stanje šefa.

## 8. Sučelje i stanja igre

Tok stanja je:

`Main Menu → Instructions → Playing ↔ Paused → Victory/Game Over → Replay ili Main Menu`

Kompaktni HUD prikazuje trup, odabrano oružje, val, bodove i dijagnostički FPS. Tijekom šefa dodaje njegovu traku zdravlja i fazu. Upozorenja najavljuju misiju i dolazak dreadnoughta. Svi natpisi i kontrole u igri ostaju na engleskom.

## 9. Vizualni i zvučni smjer

### Vizualni smjer

Paleta spaja mjed, tamno željezo, krem tipografiju, oksidirani cijan, upozoravajuću crvenu i olujno plavo nebo. Mode7 ravnina koristi proceduralne oblake, industrijske trake i mjedene navigacijske linije. Zračni brodovi crtaju se PyGame primitivima, a svaka klasa ima prepoznatljivu veličinu i boju. Čestice, projektili, bljeskovi i podrhtavanje komuniciraju udar.

### Zvuk

Sav zvuk sintetizira se tijekom izvođenja pomoću NumPyja. Top, raketa, pogodak, eksplozija i šteta koriste kratke tonove ili opadajući šum. Niski kontinuirani ton i puls čine glazbenu podlogu. Vanjski zvučni uzorci nisu potrebni.

## 10. Tehnička arhitektura

Arhitektura koristi Python 3.12 i PyGame petlju, a kasnije će dobiti zasebna aplikacijska stanja. `Mode7Renderer` koristi unaprijed izračunate dubine redaka i vodoravne koordinate, pretvara ih u koordinate svijeta te NumPy poljima uzorkuje teksturu bez Python petlje po pikselima. Interna slika je 640×360 i povećava se na 1280×720.

Brodovi, efekti, popravci i projektili projiciraju se iz svijeta na zaslon, sortiraju po dubini i zatim crtaju. Sudari koriste determinističke kružnice i najkraću udaljenost unutar svijeta opsega 2.048 jedinica. `WaveDirector` čita `data/waves.json`, a `data/balance.json` bilježi vrijednosti balansa. Podrijetlo budućih resursa vodit će se u `assets/manifest.csv`.

Trenutačna naredba `python -m aetherfront` pokreće PyGame prozor s internom slikom 640×360 skaliranom na 1280×720. Aplikacijska petlja, kamera, vektorizirana Mode7 projekcija, deterministički generator terena i vizualno NumPy uzorkovanje su implementirani. Proceduralni Kestrel prikazan je pri dnu zaslona, a billboard sustav crta scoutove, gunshipove, bombere, ISS Goliath, igračeve i neprijateljske projektile te repair pickup. Cannon, spread gun i raketa koriste vrijednosti štete i hlađenja iz `data/balance.json`. `waves.json` definira tri redovna vala, odgode spawnova, relativne položaje i stanke između valova. Nakon trećeg vala pojavljuje se boss susret: Goliath ima 900 HP, dvije faze i burst paljbu, a kompaktni HUD prikazuje health bar i fazu. Pogoci smanjuju zdravlje protivnika i bossa, uništenje redovnih protivnika dodaje bodove i stvara pickup, uništenje bossa dodaje 5.000 bodova i prikazuje pobjedu, a smrt igrača prikazuje game-over stanje. `AppState` sada vodi glavni izbornik, upute, igranje i pauzu, a terminalni ekran nakon pobjede ili poraza omogućuje novi pokušaj ili povratak na izbornik. Suptilni proceduralni efekti dodaju eksplozije, boss spark, muzzle flash i lokalni damage marker bez screen shakea. Proceduralni parallax sky slojevi za oblake, industrijsku izmaglicu i bliže linije crtaju se iznad horizonta s namjerno stišanim intenzitetom i pomakom. PyInstaller uspješno uključuje konfiguraciju i izrađuje ARM64 macOS `.app`; završni ZIP izradit će se nakon dovršetka igre.

### Sistemski zahtjevi

- macOS 13+ na Apple Siliconu ili Intelu; provjerena meta je M1 MacBook Air.
- Zaslon 1280×720 ili veći.
- Tipkovnica i približno 150 MB slobodnog prostora.
- Internetska veza nije potrebna.

## 11. Specifikacija razine — Siege of Brasshaven

Misija počinje upozorenjem „Defend Brasshaven”. Prvi val uči upravljanje i ritam topa. Drugi traži odabir prioriteta između brzih scoutova i gunshipova. Treći preklapa sva redovita ponašanja te potiče raspršenu paljbu i rakete. Zatim se pojavljuje dreadnought; promjena faze i dolazak pratnje čine vrhunac razine.

Proceduralna ravnina neprekidno se omata, pa igrač ne može napustiti borbeni prostor. Protivnici se pojavljuju u prednjem sektoru, a borba može prijeći granicu svijeta bez vidljivog prekida.

## 12. Ciljevi balansa i prihvata

- Očekivano trajanje sesije: 10–15 minuta.
- Dolazak šefa novom igraču: približno 6–9 minuta.
- Prosječne performanse: najmanje 55 FPS pri najvećem opterećenju.
- Pet uzastopnih igranja bez neobrađene iznimke.
- Cilj i kontrole razumljivi su bez vanjskih uputa.
- Svako oružje, protivnik, popravak i faza šefa pojavljuju se u uobičajenoj sesiji.

## 13. Razvoj, proračun i objava

Razvoj traje od 18. lipnja do 2. srpnja 2026. i procijenjen je na 66 individualnih sati. Proračun iznosi 0 €. Itch.io izdanje bit će besplatno i na engleskom, s opisom, kontrolama, zahtjevima, snimkama zaslona, videom, licencama i napomenom da je riječ o akademskom projektu P5. Odobrenje nastavnika za temu P5 i izmijenjeni individualni raspored zaprimljeno je 22. lipnja 2026.; objava slijedi nakon dovršetka aplikacije i završnih provjera.

## 14. Rizici, izvori, licence, AI i pojmovnik

Glavni aktivni rizici su performanse prikaza pod punim borbenim opterećenjem, širenje opsega, pakiranje, kasna izrada šefa, vrijeme za testiranje i licence. Administrativni rizik od izostanka odobrenja zatvoren je 22. lipnja 2026. Projektni plan određuje pragove i mjere. Resursi još nisu odabrani ni izrađeni; svaki budući resurs morat će biti evidentiran prije uporabe.

Generativni AI trenutačno se koristi prema FOI razini 4 za planiranje, strukturu projekta i početnu dokumentaciju. Buduća uporaba za kod i testove bit će zasebno evidentirana. Autor je odgovoran za odabir, ispravke, testiranje, izvore, privatnost i konačnu predaju. Tajne i osobni podaci nisu uneseni.

### Izvori

- Dokumentacija PyGamea: https://www.pygame.org/docs/
- Dokumentacija NumPyja: https://numpy.org/doc/
- Dokumentacija PyInstallera: https://pyinstaller.org/
- Zadatak P5 na sustavu ELF: https://elf.foi.hr/mod/page/view.php?id=137786

### Pojmovnik

- **Billboard:** 2D prikaz skaliran i postavljen kao objekt u 3D prostoru.
- **Mode7:** perspektivni dojam ravnine nastao transformacijom uzorkovanja teksture po recima zaslona.
- **Vertikalni presjek:** mala, dovršena i reprezentativna inačica konačnog proizvoda.
- **Hlađenje:** minimalno vrijeme između dviju aktivacija oružja.
- **Zamrzavanje funkcionalnosti:** trenutak nakon kojeg se više ne dodaju nove mogućnosti.

### Povijest promjena

| Verzija | Datum | Autor | Promjena |
|---|---|---|---|
| 0.1 | 18. 6. 2026. | Robert Domgjonaj | Početni koncept P5 i zaključani opseg |
| 0.2 | 19. 6. 2026. | Robert Domgjonaj | Početni GDD usklađen sa stanjem prije implementacije |
| 0.3 | 19. 6. 2026. | Robert Domgjonaj | Evidentirana implementirana aplikacijska osnova |
| 0.4 | 19. 6. 2026. | Robert Domgjonaj | Evidentirana upravljiva kamera i omatanje svijeta |
| 0.5 | 19. 6. 2026. | Robert Domgjonaj | Evidentirana Mode7 projekcijska matematika i novi rok |
| 0.6 | 19. 6. 2026. | Robert Domgjonaj | Evidentiran proceduralni generator teksture terena |
| 0.7 | 20. 6. 2026. | Robert Domgjonaj | Evidentiran vizualni Mode7 renderer i mjerenje performansi |
| 0.8 | 22. 6. 2026. | Robert Domgjonaj | Evidentirani billboard sustav, Kestrel i rani macOS paket |
| 0.9 | 22. 6. 2026. | Robert Domgjonaj | Evidentirani projektili, sudari, zdravlje i konfiguracija balansa |
| 1.0 | 22. 6. 2026. | Robert Domgjonaj | Evidentirano odobrenje teme P5 i izmijenjenog rasporeda |
| 1.1 | 22. 6. 2026. | Robert Domgjonaj | Evidentirana tri oružja, trening-cilj, repair pickup i HUD |
| 1.2 | 23. 6. 2026. | Robert Domgjonaj | Evidentirani scout, gunship i bomber kao standardni protivnici |
| 1.3 | 23. 6. 2026. | Robert Domgjonaj | Evidentirana tri konfigurirana redovna vala |
| 1.4 | 23. 6. 2026. | Robert Domgjonaj | Evidentiran ISS Goliath boss model, prikaz, HUD i dvije faze |
| 1.5 | 23. 6. 2026. | Robert Domgjonaj | Evidentiran završetak borbenog toka pobjedom ili porazom |
| 1.6 | 23. 6. 2026. | Robert Domgjonaj | Evidentirani glavni izbornik, upute, pauza i restart toka |
| 1.7 | 23. 6. 2026. | Robert Domgjonaj | Evidentiran suptilni proceduralni vizualni feedback |
| 1.8 | 23. 6. 2026. | Robert Domgjonaj | Evidentirana priprema proceduralnih parallax sky slojeva |
| 1.9 | 23. 6. 2026. | Robert Domgjonaj | Evidentirana integracija parallax sky slojeva u renderer |
| 1.10 | 23. 6. 2026. | Robert Domgjonaj | Evidentirano stišavanje parallax efekta i smanjenje borbenog HUD-a |
