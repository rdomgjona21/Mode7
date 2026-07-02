# Završni kontrolni popis prihvata

**Projekt:** Aetherfront: Zeppelin Wars  
**Datum:** 2. srpnja 2026.  
**Commit provjere:** najnoviji commit na `main` nakon završnog statusnog usklađivanja  
**Status:** release kandidat; package/ZIP provjera i PDF dokumenti završeni, prezentacija se izrađuje naknadno

## Automatizirane provjere

| Kriterij | Status | Dokaz |
|---|---|---|
| Ruff i Pytest prolaze | Prolazi | `PATH=.venv/bin:$PATH ./scripts/validate.sh` — `190 passed` |
| Mode7 renderer prelazi 55 FPS | Prolazi | `python scripts/benchmark_mode7.py --duration 12 --minimum 55` — `156.4 FPS` |
| Testovi pokrivaju osnovni state flow | Prolazi | `tests/test_game.py`, `tests/test_states.py`, `tests/test_session.py` |
| Testovi pokrivaju Mode7, sudare, oružja, valove i bossa | Prolazi | `tests/test_mode7.py`, `tests/test_collisions.py`, `tests/test_weapons.py`, `tests/test_waves.py`, `tests/test_boss.py` |
| Asset manifesti i audio/image resursi se provjeravaju | Prolazi | `tests/test_audio.py`, `tests/test_terrain.py` |
| macOS `.app` build prolazi | Prolazi | `PATH=.venv/bin:$PATH ./scripts/package.sh` |
| Release ZIP nastaje | Prolazi | `dist/Aetherfront-Zeppelin-Wars-macOS.zip`, približno 29 MB |
| Završni PDF dokumenti postoje | Prolazi | `docs/project-plan.pdf`, `docs/gdd.pdf`, `docs/technical-documentation.pdf`, `docs/testing-report.pdf`, `docs/changelog.pdf` |

## Ručne provjere

| Kriterij | Status | Napomena |
|---|---|---|
| Pokretanje iz izvornog koda | Prolazi | `python -m aetherfront` otvara glavni izbornik. |
| Main Menu → Instructions → Playing | Prolazi | Ekrani su dostupni tipkama iz README-a. |
| Playing → Paused → Resume | Prolazi | Pauza ne ruši simulaciju. |
| Restart i povratak u menu nakon završetka | Prolazi | Provjereno kroz ručne sesije. |
| Tri redovna vala | Prolazi | Wave 1, 2 i 3 pojavljuju se redom. |
| Tri oružja | Prolazi | Cannon, spread gun i rockets su vidljivi i funkcionalni. |
| Tri standardna protivnika | Prolazi | Scout, gunship i bomber pojavljuju se u normalnoj sesiji. |
| Repair pickup | Prolazi | Health i zeleni/cijan feedback aktiviraju se pri skupljanju. |
| Boss s dvije faze | Prolazi | ISS Goliath prelazi u phase 2 i prikazuje boss HUD. |
| Victory ili game-over završni ekran | Prolazi | Završni panel omogućuje restart ili menu. |
| SFX i glazba | Prolazi | Oružja, UI, repair, boss i glazbeni loopovi su čujni. |
| Pet i više ručnih sesija bez neobrađene iznimke | Prolazi | Autor je potvrdio 2. srpnja 2026. |

## Package/ZIP smoke test

| Kriterij | Status | Napomena |
|---|---|---|
| `.app` executable postoji | Prolazi | `Aetherfront.app/Contents/MacOS/Aetherfront` je izvršan. |
| ZIP se može raspakirati u čistu mapu | Prolazi | Testirano u `/tmp/aetherfront_zip_test.*`. |
| Raspakirani paket sadrži konfiguraciju | Prolazi | `balance.json` je pronađen u bundleu. |
| Raspakirani paket sadrži glazbu | Prolazi | `assets/audio/music/menu.wav` je pronađen u bundleu. |
| Raspakirani paket sadrži cloud texture asset | Prolazi | `assets/images/terrain/cloud_layer.png` je pronađen u bundleu. |
| Raspakirani executable ne pada odmah | Prolazi | Pokrenut 3 sekunde s dummy SDL video/audio driverima i zaustavljen bez ranog pada. |

## Stavke koje još treba zatvoriti prije konačne predaje

- Prezentaciju izraditi naknadno prema posebnoj odluci.
