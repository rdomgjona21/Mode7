"""Osnovna PyGame aplikacija i njezina glavna petlja."""

import math

import pygame

from aetherfront.config import (
    BACKGROUND_COLOR,
    CONTROLS_LABEL,
    INTERNAL_SIZE,
    PROTOTYPE_LABEL,
    TARGET_FPS,
    TEXT_COLOR,
    WINDOW_SIZE,
    WINDOW_TITLE,
)
from aetherfront.rendering.camera import Camera
from aetherfront.rendering.renderer import Mode7Renderer


class Game:
    """Upravlja prozorom, crtanjem i životnim ciklusom aplikacije."""

    @staticmethod
    def _axis(positive: bool, negative: bool) -> float:
        """Pretvori par tipki u os od -1 do 1; suprotne tipke međusobno se poništavaju."""
        return float(positive) - float(negative)

    @staticmethod
    def _draw_scene(
        canvas: pygame.Surface,
        font: pygame.font.Font,
        camera: Camera,
        renderer: Mode7Renderer,
        fps: float,
    ) -> None:
        """Nacrtaj Mode7 ravninu i dijagnostičko stanje kamere."""
        renderer.draw(canvas, camera)
        lines = (
            PROTOTYPE_LABEL,
            CONTROLS_LABEL,
            f"Position: {camera.x:07.2f}, {camera.y:07.2f}",
            f"Speed: {camera.speed:05.2f}",
            f"Heading: {math.degrees(camera.heading):06.2f} degrees",
            f"FPS: {fps:05.1f}",
        )

        for index, text in enumerate(lines):
            shadow = font.render(text, True, BACKGROUND_COLOR)
            label = font.render(text, True, TEXT_COLOR)
            position = (13, 13 + index * 24)
            canvas.blit(shadow, (position[0] + 1, position[1] + 1))
            canvas.blit(label, position)

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
            camera = Camera()
            renderer = Mode7Renderer()

            running = True
            frame_count = 0
            while running:
                # Delta time pretvara milisekunde protekle od zadnjeg framea u sekunde.
                dt = clock.tick(TARGET_FPS) / 1000.0

                # Operacijski sustav šalje događaj QUIT kada korisnik zatvori prozor.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                keys = pygame.key.get_pressed()
                turn = self._axis(
                    keys[pygame.K_d] or keys[pygame.K_RIGHT],
                    keys[pygame.K_a] or keys[pygame.K_LEFT],
                )
                throttle = self._axis(
                    keys[pygame.K_w] or keys[pygame.K_UP],
                    keys[pygame.K_s] or keys[pygame.K_DOWN],
                )
                camera.update(dt, turn, throttle)

                # Mode7 renderer pretvara položaj i smjer kamere u perspektivnu ravninu.
                self._draw_scene(canvas, font, camera, renderer, clock.get_fps())

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
