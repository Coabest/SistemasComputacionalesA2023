import pathlib

import pygame

# Battery
BATTERY = 100
BATTERY_DISCOUNT = 3

# Size of the square tiles used in this environment.
TILE_SIZE = 32

# Grid
ROWS = 16
COLS = 16

NUM_TILES = ROWS * COLS
NUM_ACTIONS = 4
INITIAL_STATE = 0
FINAL_STATE = ROWS*COLS - 1

# Resolution to emulate
VIRTUAL_WIDTH = TILE_SIZE * COLS
VIRTUAL_HEIGHT = TILE_SIZE * ROWS

# Scale factor between virtual screen and window
H_SCALE = 1.5
V_SCALE = 1.5

# Resolution of the actual window
WINDOW_WIDTH = VIRTUAL_WIDTH * H_SCALE
WINDOW_HEIGHT = VIRTUAL_HEIGHT * V_SCALE

# Default pause time between steps (in seconds)
DEFAULT_DELAY = 0.2

BASE_DIR = pathlib.Path(__file__).parent

# Textures used in the environment
ROBOT_FRAMES = 5
FLOOR_FRAMES = 6
TEXTURES = {
    'robot': [
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot0.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot20.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot40.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot60.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot80.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot100.png")
    ],
    'floor': [
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "floor_0.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "floor_1.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "floor_2.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "floor_3.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "floor_4.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "floor_5.png"),
    ],
    'checkpoint': pygame.image.load(BASE_DIR / "assets" / "graphics" / "checkpoint.png"),
}

# Initializing the mixer
pygame.mixer.init()

# Loading music
pygame.mixer.music.unload()
pygame.mixer.music.load(BASE_DIR / "assets" / "sounds" / "retro_music.ogg")
pygame.mixer.music.set_volume(0.5)

# Sound effects
SOUNDS = {
    'power_up': pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "power_up.ogg"),
    'power_down': pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "power_down.ogg"),
}