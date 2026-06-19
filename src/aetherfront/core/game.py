"""PyGame application shell."""

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
    """Own the window and the main application loop."""

    def run(self, max_frames: int | None = None) -> int:
        """Run until the window closes or an optional test frame limit is reached."""
        if max_frames is not None and max_frames < 1:
            raise ValueError("max_frames must be at least 1")

        pygame.init()
        try:
            window = pygame.display.set_mode(WINDOW_SIZE)
            pygame.display.set_caption(WINDOW_TITLE)
            canvas = pygame.Surface(INTERNAL_SIZE)
            clock = pygame.time.Clock()
            font = pygame.font.Font(None, 32)
            label = font.render(PROTOTYPE_LABEL, True, TEXT_COLOR)
            label_position = label.get_rect(center=(INTERNAL_SIZE[0] // 2, INTERNAL_SIZE[1] // 2))

            running = True
            frame_count = 0
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                canvas.fill(BACKGROUND_COLOR)
                canvas.blit(label, label_position)
                pygame.transform.scale(canvas, WINDOW_SIZE, window)
                pygame.display.flip()

                frame_count += 1
                if max_frames is not None and frame_count >= max_frames:
                    running = False
                clock.tick(TARGET_FPS)
        finally:
            pygame.quit()

        return 0
