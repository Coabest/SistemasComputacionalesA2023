from pathlib import Path

import pygame

from .src.frames import generate_frames

TILE_SIZE = 16
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 18

BASE_DIR = Path(__file__).parent

ENVIRONMENT = BASE_DIR / "env.txt"

# Graphics
GAME_TEXTURES = {
    "ice": pygame.image.load(BASE_DIR / "graphics" / "ice.png"),
    "snow": pygame.image.load(BASE_DIR / "graphics" / "snow.png"),
    "box": pygame.image.load(BASE_DIR / "graphics" / "box.png"),
    "character": pygame.image.load(BASE_DIR / "graphics" / "character.png"),
    "switch": pygame.image.load(BASE_DIR / "graphics" / "switch.png"),
}

# Frames
GAME_FRAMES = {
    "ice": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "snow": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "box": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "character": generate_frames(
        GAME_TEXTURES["character"], PLAYER_WIDTH, PLAYER_HEIGHT
    ),
}
