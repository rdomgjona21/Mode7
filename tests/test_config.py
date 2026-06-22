from aetherfront import config


def test_display_configuration() -> None:
    """Zaključaj osnovne dimenzije i tekst kako ih promjena ne bi slučajno narušila."""
    assert config.INTERNAL_SIZE == (640, 360)
    assert config.WINDOW_SIZE == (1280, 720)
    assert config.TARGET_FPS == 60
    assert config.WORLD_SIZE == 2048.0
    assert config.MIN_SPEED == 20.0
    assert config.MAX_SPEED == 92.0
    assert config.TURN_RATE == 1.65
    assert config.HORIZON_Y == 135
    assert config.CAMERA_HEIGHT == 50.0
    assert config.HORIZONTAL_FOV_DEGREES == 60.0
    assert config.MAX_VIEW_DISTANCE == 1400.0
    assert config.PLAYER_SURFACE_SIZE == (96, 64)
    assert config.PLAYER_SCREEN_CENTER_X == 320
    assert config.PLAYER_SCREEN_BOTTOM == 344
    assert config.PROTOTYPE_LABEL == "Technical Prototype"
