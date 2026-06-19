"""Osnovna PyGame aplikacija i njezina glavna petlja."""

import pygame

from aetherfront.config import (
    BACKGROUND_COLOR,
    INTERNAL_SIZE,
    PROTOTYPE_LABEL,
    TARGET_FPS,
    TEXT_COLOR,
    WINDOW_SIZE,
    WINDOW_TITLE,
)


class Game:
    """Upravlja prozorom, crtanjem i životnim ciklusom aplikacije."""

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
            font = pygame.font.Font(None, 32)
            label = font.render(PROTOTYPE_LABEL, True, TEXT_COLOR)
            label_position = label.get_rect(center=(INTERNAL_SIZE[0] // 2, INTERNAL_SIZE[1] // 2))

            running = True
            frame_count = 0
            while running:
                # Operacijski sustav šalje događaj QUIT kada korisnik zatvori prozor.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Svaki frame ponovno se crta od pozadine prema sadržaju.
                canvas.fill(BACKGROUND_COLOR)
                canvas.blit(label, label_position)

                # Interna slika povećava se na prozor, a flip prikazuje dovršeni frame.
                pygame.transform.scale(canvas, WINDOW_SIZE, window)
                pygame.display.flip()

                frame_count += 1
                if max_frames is not None and frame_count >= max_frames:
                    running = False

                # Bez ovog ograničenja petlja bi koristila procesor najvećom mogućom brzinom.
                clock.tick(TARGET_FPS)
        finally:
            # ``finally`` se izvodi i nakon pogreške, pa PyGame ne ostavlja aktivan prozor.
            pygame.quit()

        # Izlazni kod 0 označava uspješno završavanje programa.
        return 0
