import pygame

from .. import settings


class Map:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.width = self.cols * settings.TILE_SIZE
        self.height = self.rows * settings.TILE_SIZE
        self.charmap = [['' for _ in range(self.cols)] for _ in range(self.rows)]
    
    def render(self, surface):
        for i in range(self.rows):
            y = i * settings.TILE_SIZE
            for j in range(self.cols):
                x = j * settings.TILE_SIZE         
                if self.charmap[i][j] == '#':
                    pygame.draw.rect(surface, (0, 0, 255), pygame.Rect(x, y, settings.TILE_SIZE, settings.TILE_SIZE))
