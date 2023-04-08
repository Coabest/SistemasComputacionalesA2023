from pathlib import Path

import pygame

from .src.frames import generate_frames

TILE_SIZE = 16
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 18
STATUE_WIDTH = 16
STATUE_HEIGHT = 18

BASE_DIR = Path(__file__).parent

ENVIRONMENT = BASE_DIR / "env.txt"

# Graphics
GAME_TEXTURES = {
    "background": pygame.image.load(BASE_DIR / "graphics" / "background.png"),
    "tiles": pygame.image.load(BASE_DIR / "graphics" / "sheet.png"),
    "main_character": pygame.image.load(BASE_DIR / "graphics" / "main_character.png"),
    "statues": pygame.image.load(BASE_DIR / "graphics" / "statues.png"),
}

# Frames
GAME_FRAMES = {
    "tiles": generate_frames(GAME_TEXTURES["tiles"], TILE_SIZE, TILE_SIZE),
    "main_character": generate_frames(
        GAME_TEXTURES["main_character"], PLAYER_WIDTH, PLAYER_HEIGHT
    ),
    "statues": generate_frames(GAME_TEXTURES["statues"], STATUE_WIDTH, STATUE_HEIGHT),
}
