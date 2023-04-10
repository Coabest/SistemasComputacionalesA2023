from .. import settings

from .Entity import Entity
from .Tilemap import TileMap


class Box(Entity):
    def __init__(self, x, y, scene):
        super().__init__(x, y, settings.TILE_SIZE, settings.TILE_SIZE, "box", 0, scene)

    def push(self, di, dj):
        i, j = TileMap.to_map(self.x, self.y)

        self.tile_map.tiles[i][j].busy = False

        while (
            not self.tile_map.tiles[i + di][j + dj].busy
            and self.tile_map.map[i + di][j + dj] == "I"
        ):
            i += di
            j += dj

        self.x, self.y = TileMap.to_screen(i, j)
        self.tile_map.tiles[i][j].busy = True
