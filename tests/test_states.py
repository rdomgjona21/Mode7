from aetherfront.core.game import Game
from aetherfront.core.states import AppState


def test_app_state_values_are_stable_for_debugging() -> None:
    assert AppState.MAIN_MENU.value == "main_menu"
    assert AppState.INSTRUCTIONS.value == "instructions"
    assert AppState.PLAYING.value == "playing"
    assert AppState.PAUSED.value == "paused"


def test_new_attempt_resets_camera_and_combat_session() -> None:
    camera, session = Game._new_attempt()
    session.score = 999
    session.victory = True

    new_camera, new_session = Game._new_attempt()

    assert new_camera is not camera
    assert new_session is not session
    assert new_session.score == 0
    assert not new_session.victory
    assert not new_session.game_over
    assert new_session.enemies_remaining == 1
