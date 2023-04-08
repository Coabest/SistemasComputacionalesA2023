import pygame

from typing import TypeVar

from .. import settings

from .Entity import Entity
from .Tilemap import TileMap


class Character(Entity):
    def __init__(self, x, y, scene):
        super().__init__(
            x, y, settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT, "character", 1, scene
        )
        self.direction = 3
        self.frames_map = [10, 7, 4, 1]

    def move(self):
        self.frame_index = self.frames_map[self.direction]
        i, j = TileMap.to_map(self.x, self.y)
        n_i, n_j = i + self.off_set_i, j + self.off_set_j
        if (
            0 <= n_i < self.tile_map.rows
            and 0 <= n_j < self.tile_map.cols
            and not self.tile_map.tiles[n_i][n_j].busy
        ):
            self.x, self.y = TileMap.to_screen(n_i, n_j)

    def move_right(self, action):
        self.direction = action
        self.off_set_i = 0
        self.off_set_j = 1
        self.move()

    def move_left(self, action):
        self.direction = action
        self.off_set_i = 0
        self.off_set_j = -1
        self.move()

    def move_up(self, action):
        self.direction = action
        self.off_set_i = -1
        self.off_set_j = 0
        self.move()

    def move_down(self, action):
        self.direction = action
        self.off_set_i = 1
        self.off_set_j = 0
        self.move()

    def render(self, surface):
        texture = settings.GAME_TEXTURES[self.texture_name]
        frame = settings.GAME_FRAMES[self.texture_name][self.frame_index]
        image = pygame.Surface((frame.width, frame.height), pygame.SRCALPHA)
        image.fill((0, 0, 0, 0))
        image.blit(texture, (0, 0), frame)
        surface.blit(image, (self.x, self.y - 6))
