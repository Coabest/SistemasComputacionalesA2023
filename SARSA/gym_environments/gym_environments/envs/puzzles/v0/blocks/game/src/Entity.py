from .DrawableMixin import DrawableMixin
from .Tilemap import TileMap


class Entity(DrawableMixin):
    def __init__(self, x, y, width, height, texture_name, frame_index, scene):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_name = texture_name
        self.frame_index = frame_index
        self.scene = scene
        self.tile_map = self.scene.tile_map
