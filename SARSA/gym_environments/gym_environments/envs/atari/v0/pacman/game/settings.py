from pathlib import Path

import pygame

from .src import frames

SQUARE_MAP_SIZE = 11
TILE_SIZE = 32

VIRTUAL_WIDTH = SQUARE_MAP_SIZE * TILE_SIZE
VIRTUAL_HEIGHT = SQUARE_MAP_SIZE * TILE_SIZE
WINDOW_WIDTH = VIRTUAL_WIDTH * 2
WINDOW_HEIGHT = VIRTUAL_HEIGHT * 2

BASE_DIR = Path(__file__).parent

CHARMAP = BASE_DIR / "maps" / "level1.txt"

TEXTURES = {
    'pacman': pygame.image.load(BASE_DIR / "graphics" / "pacman.png"),
    'ghosts': pygame.image.load(BASE_DIR / "graphics" / "ghosts.png"),
}

FRAMES = {
    'pacman': frames.generate_frames(TEXTURES['pacman'], TILE_SIZE, TILE_SIZE),
    'ghosts': frames.generate_frames(TEXTURES['ghosts'], TILE_SIZE, TILE_SIZE),
}
