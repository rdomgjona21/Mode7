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
    assert config.PROTOTYPE_LABEL == "Technical Prototype"
