"""Osnovna PyGame aplikacija i njezina glavna petlja."""

import pygame

from aetherfront.config import (
    CONTROLS_LABEL,
    INTERNAL_SIZE,
    PLAYER_SCREEN_BOTTOM,
    PLAYER_SCREEN_CENTER_X,
    TARGET_FPS,
    WINDOW_SIZE,
    WINDOW_TITLE,
)
from aetherfront.core.states import AppState
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
    def _draw_scene(
        canvas: pygame.Surface,
        hud_font: pygame.font.Font,
        controls_font: pygame.font.Font,
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

        player_rect = player_surface.get_rect(
            centerx=PLAYER_SCREEN_CENTER_X,
            bottom=PLAYER_SCREEN_BOTTOM,
        )
        canvas.blit(player_surface, player_rect)
        effects.draw(canvas, camera, billboard_projector)
        draw_hud(canvas, hud_font, session, camera.speed, fps)
        controls = controls_font.render(CONTROLS_LABEL, True, (232, 220, 181))
        controls_rect = controls.get_rect(center=(INTERNAL_SIZE[0] // 2, 349))
        canvas.blit(controls, controls_rect)

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
            controls_font = pygame.font.Font(None, 22)
            camera = Camera()
            renderer = Mode7Renderer()
            billboard_projector = BillboardProjector()
            app_state = AppState.MAIN_MENU
            camera, session = self._new_attempt()
            projectile_surfaces = create_projectile_surfaces()
            enemy_surfaces = create_enemy_surfaces()
            boss_surface = create_boss_surface()
            repair_surface = create_repair_surface()
            player_surface = create_kestrel_surface()
            effects = EffectsState()

            running = True
            frame_count = 0
            while running:
                # Delta time pretvara milisekunde protekle od zadnjeg framea u sekunde.
                dt = clock.tick(TARGET_FPS) / 1000.0

                # Operacijski sustav šalje događaj QUIT kada korisnik zatvori prozor.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if app_state == AppState.MAIN_MENU:
                            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                                camera, session = self._new_attempt()
                                app_state = AppState.PLAYING
                            elif event.key == pygame.K_i:
                                app_state = AppState.INSTRUCTIONS
                            elif event.key == pygame.K_ESCAPE:
                                running = False
                        elif app_state == AppState.INSTRUCTIONS:
                            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                                camera, session = self._new_attempt()
                                app_state = AppState.PLAYING
                            elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                                app_state = AppState.MAIN_MENU
                        elif app_state == AppState.PAUSED:
                            if event.key == pygame.K_ESCAPE:
                                app_state = AppState.PLAYING
                            elif event.key == pygame.K_r:
                                camera, session = self._new_attempt()
                                app_state = AppState.PLAYING
                            elif event.key == pygame.K_m:
                                camera, session = self._new_attempt()
                                app_state = AppState.MAIN_MENU
                        elif app_state == AppState.PLAYING:
                            if session.victory or session.game_over:
                                if event.key == pygame.K_r:
                                    camera, session = self._new_attempt()
                                elif event.key == pygame.K_m:
                                    camera, session = self._new_attempt()
                                    app_state = AppState.MAIN_MENU
                            elif event.key == pygame.K_ESCAPE:
                                app_state = AppState.PAUSED
                            elif event.key == pygame.K_1:
                                session.select_primary(PrimaryWeapon.CANNON)
                            elif event.key == pygame.K_2:
                                session.select_primary(PrimaryWeapon.SPREAD)

                keys = pygame.key.get_pressed()
                turn = self._axis(
                    keys[pygame.K_d] or keys[pygame.K_RIGHT],
                    keys[pygame.K_a] or keys[pygame.K_LEFT],
                )
                throttle = self._axis(
                    keys[pygame.K_w] or keys[pygame.K_UP],
                    keys[pygame.K_s] or keys[pygame.K_DOWN],
                )
                if app_state == AppState.PLAYING and not session.victory and not session.game_over:
                    camera.update(dt, turn, throttle)
                    session.update(
                        dt,
                        camera,
                        fire_primary=keys[pygame.K_SPACE],
                        fire_rocket=keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT],
                    )
                    for x, y in session.feedback.destroyed_positions:
                        effects.add_explosion(x, y)
                    for x, y in session.feedback.repair_collected_positions:
                        effects.add_repair_flash(x, y)
                    if session.feedback.boss_was_hit and session.boss is not None:
                        effects.add_boss_spark(session.boss.x, session.boss.y)
                    if session.feedback.player_was_damaged:
                        effects.trigger_player_hit()
                    if session.feedback.player_fired:
                        effects.trigger_muzzle_flash()
                    effects.update(dt)

                # Mode7 renderer pretvara položaj i smjer kamere u perspektivnu ravninu.
                self._draw_scene(
                    canvas,
                    hud_font,
                    controls_font,
                    camera,
                    renderer,
                    billboard_projector,
                    session,
                    projectile_surfaces,
                    enemy_surfaces,
                    boss_surface,
                    repair_surface,
                    player_surface,
                    clock.get_fps(),
                    effects,
                )
                self._draw_overlay(canvas, font, app_state, session)

                # Interna slika povećava se na prozor, a flip prikazuje dovršeni frame.
                pygame.transform.scale(canvas, WINDOW_SIZE, window)
                pygame.display.flip()

                frame_count += 1
                if max_frames is not None and frame_count >= max_frames:
                    running = False
        finally:
            # ``finally`` se izvodi i nakon pogreške, pa PyGame ne ostavlja aktivan prozor.
            pygame.quit()

        # Izlazni kod 0 označava uspješno završavanje programa.
        return 0
