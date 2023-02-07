import pygame
import numpy as np
from . import settingss


class Tile:
    def __init__(self, x, y, texture_name, frame=None):
        self.x = x
        self.y = y
        self.texture_name = texture_name
        self.frame = frame

    def render(self, surface):
        if self.frame == None:
            surface.blit(settingss.TEXTURES[self.texture_name], (self.x, self.y))
        else:
            surface.blit(settingss.TEXTURES[self.texture_name][self.frame], (self.x, self.y))



class TileMap:
    def __init__(self, tile_texture_names, frame=None):
        self.tiles = []
        tile_counter = 0
        for i in range(settingss.ROWS):
            for j in range(settingss.COLS):
                self.tiles.append(
                    Tile(
                        j * settingss.TILE_SIZE,
                        i * settingss.TILE_SIZE,
                        tile_texture_names[tile_counter],
                        np.random.randint(0,settingss.FLOOR_FRAMES))
                )
                tile_counter += 1

    def render(self, surface):
        for tile in self.tiles:
            tile.render(surface)
