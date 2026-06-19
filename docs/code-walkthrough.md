# Vodič kroz trenutačni kod

Ovaj dokument objašnjava aplikacijsku osnovu prije uvođenja kamere, Mode7 prikaza i
gameplaya. Najlakše ju je razumjeti praćenjem redoslijeda kojim Python izvodi kod.

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

## 3. Glavna petlja

`Game.run()` prvo provjerava testni argument `max_frames`, zatim inicijalizira PyGame.
Blok `try/finally` jamči poziv `pygame.quit()` čak i ako se tijekom izvođenja dogodi
iznimka.

Postoje dvije površine:

- `window` je stvarni prozor veličine 1280×720;
- `canvas` je interna slika veličine 640×360 na kojoj se crta sadržaj.

Petlja `while running` čini jedan frame u svakom prolazu:

1. čita događaje operacijskog sustava;
2. prekida rad nakon događaja `QUIT`;
3. briše prethodni frame bojom pozadine;
4. crta tekst na internu površinu;
5. povećava internu površinu na prozor;
6. prikazuje dovršenu sliku pozivom `pygame.display.flip()`;
7. ograničava petlju na 60 FPS.

`max_frames` se koristi samo u testovima kako bi se petlja sama zaustavila. U normalnom
pokretanju vrijednost je `None`, pa aplikacija radi dok korisnik ne zatvori prozor.

## 4. Automatizirani testovi

`test_config.py` provjerava da ključne postavke imaju očekivane vrijednosti.
`test_game.py` koristi SDL upravljačke programe `dummy`, zbog čega PyGame može izvesti
frame bez stvarnog prozora i zvučnog uređaja. Test zatim potvrđuje izlazni kod `0` i da
je PyGame uredno ugašen.

Drugi test šalje neispravnu vrijednost `max_frames=0` i očekuje `ValueError`. Time se
provjerava i ponašanje u slučaju pogrešnog poziva, a ne samo uspješan slučaj.

## 5. Validacija

`scripts/validate.sh` pokreće dvije provjere. Ruff provjerava stil, uvoze i česte Python
pogreške. Pytest izvršava sve funkcije čiji naziv počinje s `test_`. Postavka
`set -euo pipefail` zaustavlja skriptu čim neka provjera ne uspije.

Za učenje je korisno privremeno promijeniti jednu konstantu ili očekivanje u testu,
pokrenuti `./scripts/validate.sh`, pročitati pogrešku i zatim vratiti promjenu.
