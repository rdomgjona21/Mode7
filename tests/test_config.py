from aetherfront import config


def test_display_configuration() -> None:
    assert config.INTERNAL_SIZE == (640, 360)
    assert config.WINDOW_SIZE == (1280, 720)
    assert config.TARGET_FPS == 60
    assert config.PROTOTYPE_LABEL == "Technical Prototype"
