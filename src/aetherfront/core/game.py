"""Osnovna PyGame aplikacija i njezina glavna petlja."""

from dataclasses import dataclass

import pygame

from aetherfront.audio.manager import AudioManager, MusicTrack, SoundEffect
from aetherfront.config import (
    INTERNAL_SIZE,
    PLAYER_SCREEN_BOTTOM,
    PLAYER_SCREEN_CENTER_X,
    TARGET_FPS,
    WINDOW_SIZE,
    WINDOW_TITLE,
)
from aetherfront.core.states import AppState
from aetherfront.gameplay.boss import BossPhase
from aetherfront.gameplay.enemies import EnemyKind
from aetherfront.gameplay.session import CombatSession
from aetherfront.gameplay.weapons import PrimaryWeapon
from aetherfront.rendering.billboards import BillboardProjector, WorldBillboard
from aetherfront.rendering.camera import Camera
from aetherfront.rendering.combat_sprites import (
    create_boss_surface,
    create_enemy_surfaces,
    create_projectile_surfaces,
    create_repair_surface,
)
from aetherfront.rendering.effects import EffectsState
from aetherfront.rendering.renderer import Mode7Renderer
from aetherfront.rendering.ships import create_kestrel_surface
from aetherfront.ui.hud import draw_hud
from aetherfront.ui.menus import (
    draw_instructions,
    draw_main_menu,
    draw_pause_menu,
    draw_terminal_menu,
)


@dataclass(slots=True)
class GameRuntimeState:
    """Promjenjivo stanje aplikacije koje event handleri mogu ažurirati."""

    app_state: AppState
    camera: Camera
    session: CombatSession
    terminal_audio_played: str | None = None
    running: bool = True


class Game:
    """Upravlja prozorom, crtanjem i životnim ciklusom aplikacije."""

    @staticmethod
    def _axis(positive: bool, negative: bool) -> float:
        """Pretvori par tipki u os od -1 do 1; suprotne tipke međusobno se poništavaju."""
        return float(positive) - float(negative)

    @staticmethod
    def _new_attempt() -> tuple[Camera, CombatSession]:
        """Stvori svježu kameru i borbenu sesiju za novi pokušaj misije."""
        camera = Camera()
        return camera, CombatSession.create(camera)

    @staticmethod
    def _start_attempt(state: GameRuntimeState) -> None:
        """Resetiraj kameru i borbu te prebaci aplikaciju u igranje."""
        state.camera, state.session = Game._new_attempt()
        state.terminal_audio_played = None
        state.app_state = AppState.PLAYING

    @staticmethod
    def _return_to_menu(state: GameRuntimeState, audio: AudioManager) -> None:
        """Vrati aplikaciju u menu s čistim pokušajem i ugašenom borbenom glazbom."""
        state.camera, state.session = Game._new_attempt()
        state.terminal_audio_played = None
        audio.stop_music()
        state.app_state = AppState.MAIN_MENU

    @staticmethod
    def _handle_menu_event(
        event: pygame.event.Event,
        state: GameRuntimeState,
        audio: AudioManager,
    ) -> None:
        """Obradi tipke dostupne na glavnom izborniku."""
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            audio.play(SoundEffect.MENU_SELECT)
            Game._start_attempt(state)
        elif event.key == pygame.K_i:
            audio.play(SoundEffect.MENU_SELECT)
            state.app_state = AppState.INSTRUCTIONS
        elif event.key == pygame.K_ESCAPE:
            state.running = False

    @staticmethod
    def _handle_instructions_event(
        event: pygame.event.Event,
        state: GameRuntimeState,
        audio: AudioManager,
    ) -> None:
        """Obradi tipke na ekranu uputa."""
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            audio.play(SoundEffect.MENU_SELECT)
            Game._start_attempt(state)
        elif event.key in (pygame.K_m, pygame.K_ESCAPE):
            audio.play(SoundEffect.MENU_SELECT)
            state.app_state = AppState.MAIN_MENU

    @staticmethod
    def _handle_pause_event(
        event: pygame.event.Event,
        state: GameRuntimeState,
        audio: AudioManager,
    ) -> None:
        """Obradi tipke dok je pokušaj pauziran."""
        if event.key == pygame.K_ESCAPE:
            audio.play(SoundEffect.PAUSE)
            audio.stop_music()
            state.app_state = AppState.PLAYING
        elif event.key == pygame.K_r:
            audio.play(SoundEffect.MENU_SELECT)
            Game._start_attempt(state)
        elif event.key == pygame.K_m:
            audio.play(SoundEffect.MENU_SELECT)
            Game._return_to_menu(state, audio)

    @staticmethod
    def _handle_game_event(
        event: pygame.event.Event,
        state: GameRuntimeState,
        audio: AudioManager,
    ) -> None:
        """Obradi tipke tijekom igranja i na terminalnom victory/game-over panelu."""
        if state.session.victory or state.session.game_over:
            if event.key == pygame.K_r:
                audio.play(SoundEffect.MENU_SELECT)
                Game._start_attempt(state)
            elif event.key == pygame.K_m:
                audio.play(SoundEffect.MENU_SELECT)
                Game._return_to_menu(state, audio)
            return

        if event.key == pygame.K_ESCAPE:
            audio.play(SoundEffect.PAUSE)
            audio.stop_music()
            state.app_state = AppState.PAUSED
        elif event.key == pygame.K_1:
            if state.session.weapons.primary is not PrimaryWeapon.CANNON:
                audio.play(SoundEffect.WEAPON_READY)
            state.session.select_primary(PrimaryWeapon.CANNON)
        elif event.key == pygame.K_2:
            if state.session.weapons.primary is not PrimaryWeapon.SPREAD:
                audio.play(SoundEffect.WEAPON_READY)
            state.session.select_primary(PrimaryWeapon.SPREAD)

    @staticmethod
    def _handle_keydown_event(
        event: pygame.event.Event,
        state: GameRuntimeState,
        audio: AudioManager,
    ) -> None:
        """Usmjeri KEYDOWN događaj prema handleru trenutačnog aplikacijskog stanja."""
        if state.app_state == AppState.MAIN_MENU:
            Game._handle_menu_event(event, state, audio)
        elif state.app_state == AppState.INSTRUCTIONS:
            Game._handle_instructions_event(event, state, audio)
        elif state.app_state == AppState.PAUSED:
            Game._handle_pause_event(event, state, audio)
        elif state.app_state == AppState.PLAYING:
            Game._handle_game_event(event, state, audio)

    @staticmethod
    def _handle_pygame_event(
        event: pygame.event.Event,
        state: GameRuntimeState,
        audio: AudioManager,
    ) -> None:
        """Obradi jedan PyGame event bez izravnog crtanja ili simulacije borbe."""
        if event.type == pygame.QUIT:
            state.running = False
        elif event.type == pygame.KEYDOWN:
            Game._handle_keydown_event(event, state, audio)

    @staticmethod
    def _draw_overlay(
        canvas: pygame.Surface,
        font: pygame.font.Font,
        app_state: AppState,
        session: CombatSession,
    ) -> None:
        """Nacrtaj odgovarajući ekran iznad scene."""
        if app_state == AppState.MAIN_MENU:
            draw_main_menu(canvas, font)
        elif app_state == AppState.INSTRUCTIONS:
            draw_instructions(canvas, font)
        elif app_state == AppState.PAUSED:
            draw_pause_menu(canvas, font)
        elif app_state == AppState.PLAYING:
            draw_terminal_menu(canvas, font, session)

    @staticmethod
    def _play_combat_audio(audio: AudioManager, session: CombatSession) -> None:
        """Reproduciraj SFX događaje koje je borbena sesija prijavila za zadnji frame."""
        weapon_sounds = {
            "cannon": SoundEffect.CANNON_FIRE,
            "spread": SoundEffect.SPREAD_FIRE,
            "rocket": SoundEffect.ROCKET_LAUNCH,
        }

        # Igrač može u istom frameu ispaliti primarno oružje i raketu, pa svako stvarno
        # ispaljeno oružje dobiva vlastiti kratki SFX. Ako hlađenje nije završilo,
        # `CombatSession` ga neće prijaviti i ovdje se ne reproducira zvuk.
        for weapon in session.feedback.fired_weapons:
            sound = weapon_sounds.get(weapon)
            if sound is not None:
                audio.play(sound)

        # Neprijatelji mogu ispaliti više projektila istog tipa u jednom frameu. Set čuva
        # samo vrste zvukova, pa se isti SFX ne multiplicira nepotrebno glasno.
        if "enemy_light" in session.feedback.enemy_fire_kinds:
            audio.play(SoundEffect.ENEMY_LIGHT_FIRE)
        if "enemy_heavy" in session.feedback.enemy_fire_kinds:
            audio.play(SoundEffect.ENEMY_HEAVY_FIRE)

        # Ovi događaji nisu stalna paljba, nego kratke oznake promjene stanja ili pogotka.
        if session.feedback.wave_started:
            audio.play(SoundEffect.WAVE_START)
        if session.feedback.boss_spawned:
            audio.play(SoundEffect.BOSS_ARRIVAL)
        if session.feedback.destroyed_positions:
            audio.play(SoundEffect.ENEMY_DESTROYED)
        if session.feedback.repair_collected_positions:
            audio.play(SoundEffect.REPAIR_PICKUP)
        if session.feedback.boss_was_hit:
            audio.play(SoundEffect.BOSS_HIT)
        if session.feedback.boss_destroyed:
            audio.play(SoundEffect.BOSS_DESTROYED)
        if session.feedback.player_was_damaged:
            audio.play(SoundEffect.PLAYER_DAMAGE)

    @staticmethod
    def _music_for_session(session: CombatSession) -> MusicTrack:
        """Return the looping music track for the current combat progression."""
        if session.boss is not None and session.boss.alive:
            if session.boss.phase is BossPhase.PHASE_TWO:
                return MusicTrack.BOSS_PHASE_2
            return MusicTrack.BOSS_PHASE_1

        # WaveDirector normalno vraća 1, 2 ili 3. Fallback sprječava rušenje ako test,
        # buduća izmjena ili neispravno stanje privremeno izloži broj izvan tog raspona.
        wave_music = {
            1: MusicTrack.WAVE_1,
            2: MusicTrack.WAVE_2,
            3: MusicTrack.WAVE_3,
        }
        return wave_music.get(session.wave_director.current_wave_number, MusicTrack.WAVE_1)

    @staticmethod
    def _draw_scene(
        canvas: pygame.Surface,
        hud_font: pygame.font.Font,
        camera: Camera,
        renderer: Mode7Renderer,
        billboard_projector: BillboardProjector,
        session: CombatSession,
        projectile_surfaces: dict[str, pygame.Surface],
        enemy_surfaces: dict[EnemyKind, pygame.Surface],
        boss_surface: pygame.Surface,
        repair_surface: pygame.Surface,
        player_surface: pygame.Surface,
        fps: float,
        effects: EffectsState,
    ) -> None:
        """Nacrtaj teren, borbene objekte, igrača i HUD."""
        renderer.draw(canvas, camera)
        billboards: list[WorldBillboard] = []
        # Svi svjetski objekti prvo se pretvore u `WorldBillboard` zapise. Projector ih
        # zatim sortira po dubini, pa bliži brodovi i projektili pravilno prekrivaju dalje.
        for enemy in session.enemies:
            billboards.append(
                WorldBillboard(
                    enemy_surfaces[enemy.kind],
                    enemy.x,
                    enemy.y,
                    enemy.radius * 2,
                )
            )
        if session.boss is not None and session.boss.alive:
            billboards.append(
                WorldBillboard(
                    boss_surface,
                    session.boss.x,
                    session.boss.y,
                    session.boss.radius * 2,
                )
            )
        billboards.extend(
            WorldBillboard(
                projectile_surfaces[projectile.kind],
                projectile.x,
                projectile.y,
                projectile.radius * 2,
            )
            for projectile in session.projectiles
        )
        billboards.extend(
            WorldBillboard(
                repair_surface,
                pickup.x,
                pickup.y,
                pickup.radius * 2,
            )
            for pickup in session.pickups
        )
        billboard_projector.draw(canvas, camera, billboards)

        # Igračev brod nije svjetski billboard. Kamera već predstavlja njegov položaj, pa
        # se Kestrel crta fiksno pri dnu ekrana kao cockpit/ship view.
        player_rect = player_surface.get_rect(
            centerx=PLAYER_SCREEN_CENTER_X,
            bottom=PLAYER_SCREEN_BOTTOM,
        )
        canvas.blit(player_surface, player_rect)
        # Efekti idu nakon brodova i projektila, ali prije HUD-a, kako eksplozije ne bi
        # prekrivale tekstualne informacije.
        effects.draw(canvas, camera, billboard_projector)
        draw_hud(canvas, hud_font, session, camera.speed, fps)

    def run(self, max_frames: int | None = None) -> int:
        """Izvodi aplikaciju do zatvaranja prozora ili testnog ograničenja frameova.

        ``max_frames`` je ``None`` tijekom normalnog igranja. Test ga postavlja na mali
        broj kako se automatizirana provjera ne bi izvodila beskonačno.
        """
        if max_frames is not None and max_frames < 1:
            raise ValueError("max_frames must be at least 1")

        # PyGame mora biti inicijaliziran prije izrade prozora, fonta i sata.
        pygame.init()
        try:
            # ``window`` je stvarni prozor, a ``canvas`` manja interna površina za crtanje.
            window = pygame.display.set_mode(WINDOW_SIZE)
            pygame.display.set_caption(WINDOW_TITLE)
            canvas = pygame.Surface(INTERNAL_SIZE)

            # Clock ograničava brzinu petlje, a zadani PyGame font ne traži vanjsku datoteku.
            clock = pygame.time.Clock()
            font = pygame.font.Font(None, 26)
            hud_font = pygame.font.Font(None, 20)
            camera = Camera()
            renderer = Mode7Renderer()
            billboard_projector = BillboardProjector()
            camera, session = self._new_attempt()
            state = GameRuntimeState(
                app_state=AppState.MAIN_MENU,
                camera=camera,
                session=session,
            )
            projectile_surfaces = create_projectile_surfaces()
            enemy_surfaces = create_enemy_surfaces()
            boss_surface = create_boss_surface()
            repair_surface = create_repair_surface()
            player_surface = create_kestrel_surface()
            effects = EffectsState()
            audio = AudioManager.load()

            frame_count = 0
            while state.running:
                # Delta time pretvara milisekunde protekle od zadnjeg framea u sekunde.
                dt = clock.tick(TARGET_FPS) / 1000.0

                # Operacijski sustav šalje događaj QUIT kada korisnik zatvori prozor.
                for event in pygame.event.get():
                    self._handle_pygame_event(event, state, audio)

                keys = pygame.key.get_pressed()
                turn = self._axis(
                    keys[pygame.K_d] or keys[pygame.K_RIGHT],
                    keys[pygame.K_a] or keys[pygame.K_LEFT],
                )
                throttle = self._axis(
                    keys[pygame.K_w] or keys[pygame.K_UP],
                    keys[pygame.K_s] or keys[pygame.K_DOWN],
                )
                if (
                    state.app_state == AppState.PLAYING
                    and not state.session.victory
                    and not state.session.game_over
                ):
                    state.camera.update(dt, turn, throttle)
                    state.session.update(
                        dt,
                        state.camera,
                        fire_primary=keys[pygame.K_SPACE],
                        fire_rocket=keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT],
                    )
                    for x, y in state.session.feedback.destroyed_positions:
                        effects.add_explosion(x, y)
                    for x, y in state.session.feedback.repair_collected_positions:
                        effects.add_repair_flash(x, y)
                    # `CombatFeedback` je most između gameplaya i prezentacijskog sloja:
                    # session odlučuje što se dogodilo, a Game samo pokreće efekte/zvuk.
                    if state.session.feedback.boss_was_hit and state.session.boss is not None:
                        effects.add_boss_spark(state.session.boss.x, state.session.boss.y)
                    if state.session.feedback.player_was_damaged:
                        effects.trigger_player_hit()
                    if state.session.feedback.player_fired:
                        effects.trigger_muzzle_flash()
                    audio.play_music(self._music_for_session(state.session))
                    self._play_combat_audio(audio, state.session)
                    if state.session.victory and state.terminal_audio_played != "victory":
                        # Terminalni SFX smije se pokrenuti samo jednom po pokušaju.
                        audio.play_terminal(SoundEffect.VICTORY)
                        state.terminal_audio_played = "victory"
                    elif (
                        state.session.game_over
                        and state.terminal_audio_played != "game_over"
                    ):
                        # Isto vrijedi za game-over, inače bi se zvuk ponavljao svaki frame.
                        audio.play_terminal(SoundEffect.GAME_OVER)
                        state.terminal_audio_played = "game_over"
                    effects.update(dt)
                elif state.app_state in (AppState.MAIN_MENU, AppState.INSTRUCTIONS):
                    audio.play_music(MusicTrack.MENU)

                # Mode7 renderer pretvara položaj i smjer kamere u perspektivnu ravninu.
                self._draw_scene(
                    canvas,
                    hud_font,
                    state.camera,
                    renderer,
                    billboard_projector,
                    state.session,
                    projectile_surfaces,
                    enemy_surfaces,
                    boss_surface,
                    repair_surface,
                    player_surface,
                    clock.get_fps(),
                    effects,
                )
                self._draw_overlay(canvas, font, state.app_state, state.session)

                # Interna slika povećava se na prozor, a flip prikazuje dovršeni frame.
                pygame.transform.scale(canvas, WINDOW_SIZE, window)
                pygame.display.flip()

                frame_count += 1
                if max_frames is not None and frame_count >= max_frames:
                    state.running = False
        finally:
            # ``finally`` se izvodi i nakon pogreške, pa PyGame ne ostavlja aktivan prozor.
            pygame.quit()

        # Izlazni kod 0 označava uspješno završavanje programa.
        return 0
