from .DrawableMixin import DrawableMixin
from .Tilemap import TileMap


class Entity(DrawableMixin):
    def __init__(
        self, x, y, width, height, texture_name, frame_index, world, movement, busy_mark
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_name = texture_name
        self.frame_index = frame_index
        self.world = world
        self.tile_map = self.world.tile_map
        self.off_set_i = 0
        self.off_set_j = 0
        self.movement = movement
        self.busy_mark = busy_mark

    def move(self):
        i, j = TileMap.to_map(self.x, self.y)
        n_i, n_j = i + self.off_set_i, j + self.off_set_j
        if (
            0 <= n_i < self.tile_map.rows
            and 0 <= n_j < self.tile_map.cols
            and self.tile_map.tiles[n_i][n_j].busy_by != "ST"
            and self.tile_map.map[n_i][n_j] != 0
        ):
            self.tile_map.tiles[i][j].busy_by = None
            self.tile_map.tiles[n_i][n_j].busy_by = self.busy_mark
            self.x, self.y = TileMap.to_screen(n_i, n_j)

    def move_right(self):
        self.off_set_i = 0
        self.off_set_j = 1
        self.move()

    def move_left(self):
        self.off_set_i = 0
        self.off_set_j = -1
        self.move()

    def move_up(self):
        self.off_set_i = -1
        self.off_set_j = 0
        self.move()

    def move_down(self):
        self.off_set_i = 1
        self.off_set_j = 0
        self.move()
