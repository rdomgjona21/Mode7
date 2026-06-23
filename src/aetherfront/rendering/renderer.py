"""Vizualni Mode7 renderer koji NumPy koordinatama uzorkuje teksturu terena."""

import numpy as np
import pygame

from aetherfront.config import HORIZON_Y, INTERNAL_SIZE, WORLD_SIZE
from aetherfront.rendering.camera import Camera
from aetherfront.rendering.mode7 import Mode7Projection
from aetherfront.rendering.terrain import generate_terrain_texture


class Mode7Renderer:
    """Crta nebo i perspektivnu ravninu bez Python petlje po pikselima."""

    def __init__(
        self,
        projection: Mode7Projection | None = None,
        texture: np.ndarray | None = None,
    ) -> None:
        """Pripremi projekciju, teksturu i nepromjenjivu gradaciju neba."""
        self.projection = projection or Mode7Projection()
        self.texture = generate_terrain_texture() if texture is None else texture
        self._validate_texture(self.texture)

        if (self.projection.width, self.projection.height) != INTERNAL_SIZE:
            raise ValueError("projection dimensions must match the internal display")

        self._texture_height, self._texture_width = self.texture.shape[:2]
        self._texture_scale_x = self._texture_width / WORLD_SIZE
        self._texture_scale_y = self._texture_height / WORLD_SIZE
        self._sky = self._create_sky()

    @staticmethod
    def _validate_texture(texture: np.ndarray) -> None:
        """Odbij teksturu koju PyGame ne može sigurno prikazati kao RGB sliku."""
        if texture.ndim != 3 or texture.shape[2] != 3:
            raise ValueError("terrain texture must have RGB shape (height, width, 3)")
        if texture.shape[0] < 1 or texture.shape[1] < 1:
            raise ValueError("terrain texture dimensions must be positive")
        if texture.dtype != np.uint8:
            raise ValueError("terrain texture must use uint8 values")

    @staticmethod
    def _create_sky() -> np.ndarray:
        """Stvori statičnu olujno-plavu gradaciju iznad horizonta."""
        top = np.array((18, 29, 48), dtype=np.float64)
        bottom = np.array((74, 91, 105), dtype=np.float64)
        blend = np.linspace(0.0, 1.0, HORIZON_Y + 1, dtype=np.float64)[:, np.newaxis]
        rows = top + (bottom - top) * blend
        sky = np.broadcast_to(rows[:, np.newaxis, :], (HORIZON_Y + 1, INTERNAL_SIZE[0], 3))
        return np.ascontiguousarray(sky, dtype=np.uint8)

    def sample_ground(self, camera: Camera) -> np.ndarray:
        """Vrati RGB piksele tla dobivene vektoriziranim uzorkovanjem teksture."""
        grid = self.projection.project(camera)
        texture_x = (grid.world_x * self._texture_scale_x).astype(np.intp)
        texture_y = (grid.world_y * self._texture_scale_y).astype(np.intp)
        texture_x %= self._texture_width
        texture_y %= self._texture_height
        return np.ascontiguousarray(self.texture[texture_y, texture_x])

    def draw(
        self,
        canvas: pygame.Surface,
        camera: Camera,
        shake_offset: tuple[float, float] = (0.0, 0.0),
    ) -> None:
        """Nacrtaj jedan Mode7 frame na internu PyGame površinu."""
        if canvas.get_size() != INTERNAL_SIZE:
            raise ValueError("canvas dimensions must match the internal display")

        sky_surface = canvas.subsurface((0, 0, INTERNAL_SIZE[0], HORIZON_Y + 1))
        pygame.surfarray.blit_array(sky_surface, np.swapaxes(self._sky, 0, 1))

        # Privremeno pomakni kameru za shake offset pri uzorkovanju terena.
        original_x, original_y = camera.x, camera.y
        camera.x = (camera.x + shake_offset[0]) % WORLD_SIZE
        camera.y = (camera.y + shake_offset[1]) % WORLD_SIZE
        ground = self.sample_ground(camera)
        camera.x, camera.y = original_x, original_y

        ground_surface = canvas.subsurface(
            (0, HORIZON_Y + 1, INTERNAL_SIZE[0], INTERNAL_SIZE[1] - HORIZON_Y - 1)
        )
        pygame.surfarray.blit_array(ground_surface, np.swapaxes(ground, 0, 1))
        pygame.draw.line(canvas, (194, 156, 82), (0, HORIZON_Y), (INTERNAL_SIZE[0], HORIZON_Y))
