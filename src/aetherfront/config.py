"""Zajedničke postavke aplikacije na jednom mjestu."""

# Prozor je dvostruko veći od interne slike po obje osi. Igra se crta na manjoj
# površini radi jednostavnijeg retro prikaza, a zatim povećava na stvarni prozor.
WINDOW_TITLE = "Aetherfront: Zeppelin Wars"
INTERNAL_SIZE = (640, 360)
WINDOW_SIZE = (1280, 720)
TARGET_FPS = 60

# Kamera se ne može zaustaviti: promjena brzine ostaje unutar GDD granica 20-92.
WORLD_SIZE = 2048.0
MIN_SPEED = 20.0
MAX_SPEED = 92.0
SPEED_CHANGE_RATE = 36.0
TURN_RATE = 1.65

# Mode7 projekcija počinje ispod horizonta i ograničava najudaljenije uzorke kako
# bi se izbjeglo višestruko omatanje cijelog svijeta u prvih nekoliko redaka.
HORIZON_Y = 135
CAMERA_HEIGHT = 50.0
HORIZONTAL_FOV_DEGREES = 60.0
MAX_VIEW_DISTANCE = 1400.0

# PyGame boje zapisuju se kao RGB trojke, gdje je svaka vrijednost od 0 do 255.
BACKGROUND_COLOR = (24, 35, 51)
TEXT_COLOR = (229, 215, 174)
PROTOTYPE_LABEL = "Combat Training Prototype"
CONTROLS_LABEL = "1/2 Weapon | Space Fire | Shift Rocket | A/D Steer | W/S Throttle"
PLAYER_SURFACE_SIZE = (96, 64)
PLAYER_SCREEN_CENTER_X = INTERNAL_SIZE[0] // 2
PLAYER_SCREEN_BOTTOM = 344
