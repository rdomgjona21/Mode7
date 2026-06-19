"""Vektorizirana matematika za pretvaranje piksela tla u koordinate svijeta."""

import math
from dataclasses import dataclass

import numpy as np

from aetherfront.config import (
    CAMERA_HEIGHT,
    HORIZON_Y,
    HORIZONTAL_FOV_DEGREES,
    INTERNAL_SIZE,
    MAX_VIEW_DISTANCE,
    WORLD_SIZE,
)
from aetherfront.rendering.camera import Camera


@dataclass(frozen=True, slots=True)
class ProjectionGrid:
    """Sadrži retke zaslona i koordinate svijeta za buduće uzorkovanje teksture."""

    screen_rows: np.ndarray
    world_x: np.ndarray
    world_y: np.ndarray


class Mode7Projection:
    """Predizračunava perspektivu i projicira cijelu ravninu NumPy operacijama."""

    def __init__(
        self,
        width: int = INTERNAL_SIZE[0],
        height: int = INTERNAL_SIZE[1],
        horizon: int = HORIZON_Y,
        horizontal_fov_degrees: float = HORIZONTAL_FOV_DEGREES,
        camera_height: float = CAMERA_HEIGHT,
        max_view_distance: float = MAX_VIEW_DISTANCE,
        world_size: float = WORLD_SIZE,
    ) -> None:
        """Pripremi podatke koji ovise samo o postavkama prikaza, a ne o kameri."""
        if width < 2 or height < 2:
            raise ValueError("projection dimensions must be at least 2")
        if not 0 <= horizon < height - 1:
            raise ValueError("horizon must leave at least one ground row")
        if not 0 < horizontal_fov_degrees < 180:
            raise ValueError("horizontal FOV must be between 0 and 180 degrees")
        if camera_height <= 0:
            raise ValueError("camera height must be positive")
        if max_view_distance <= 0:
            raise ValueError("maximum view distance must be positive")
        if world_size <= 0:
            raise ValueError("world size must be positive")

        self.width = width
        self.height = height
        self.horizon = horizon
        self.world_size = world_size

        fov_radians = math.radians(horizontal_fov_degrees)
        half_fov_tangent = math.tan(fov_radians / 2)
        focal_length = (width / 2) / half_fov_tangent

        # Prvi redak tla je horizon + 1 kako nazivnik nikada ne bi bio nula.
        screen_rows = np.arange(horizon + 1, height, dtype=np.int32)
        row_offsets = screen_rows.astype(np.float64) - horizon
        row_distances = camera_height * focal_length / row_offsets
        row_distances = np.minimum(row_distances, max_view_distance)

        # Središnji stupac ima bočni faktor 0; rubovi prate zadani horizontalni FOV.
        screen_x = np.arange(width, dtype=np.float64) - width // 2
        lateral_factors = screen_x / (width / 2) * half_fov_tangent

        self.screen_rows = screen_rows
        self._forward_distances = row_distances[:, np.newaxis]
        self._lateral_offsets = self._forward_distances * lateral_factors[np.newaxis, :]

        # Predizračunate vrijednosti ne smiju se slučajno mijenjati između frameova.
        self.screen_rows.setflags(write=False)
        self._forward_distances.setflags(write=False)
        self._lateral_offsets.setflags(write=False)

    def project(self, camera: Camera) -> ProjectionGrid:
        """Vrati omotane koordinate svijeta za svaki piksel tla ispod horizonta."""
        forward_x = math.cos(camera.heading)
        forward_y = math.sin(camera.heading)
        right_x = -forward_y
        right_y = forward_x

        world_x = (
            camera.x
            + forward_x * self._forward_distances
            + right_x * self._lateral_offsets
        ) % self.world_size
        world_y = (
            camera.y
            + forward_y * self._forward_distances
            + right_y * self._lateral_offsets
        ) % self.world_size

        return ProjectionGrid(
            screen_rows=self.screen_rows,
            world_x=world_x,
            world_y=world_y,
        )
