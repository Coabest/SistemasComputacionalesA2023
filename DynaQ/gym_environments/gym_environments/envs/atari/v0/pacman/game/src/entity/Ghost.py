import pygame

from .BaseEntity import BaseEntity
from ..search.Path import Path


class Ghost(BaseEntity):
    def __init__(self, x, y, w, h, speed, texture, frames, interval, scene, mode):
        animations = {
            (-1, 0): frames[2:4],
            (0, 1): frames[6:8],
            (1, 0): frames[0:2],
            (0, -1): frames[4:6],
        }
        super().__init__(x, y, w, h, speed, texture, interval, animations)
        self.current_animation = [frames[0]]
        self.scene = scene
        self.mode = mode
        self.path = Path()

    def __find_path(self):
        srcp = self.position
        srcs = self.size
        tgtp = self.scene.pacman.position
        tgts = self.scene.pacman.size
        src = (int(srcp.y // srcs.y), int(srcp.x // srcs.x))
        tgt = (int(tgtp.y // tgts.y), int(tgtp.x // tgts.x))
        self.path = self.scene.pathfinder.find_path(src, tgt, self.mode)
        
    def update(self, dt):
        super().update(dt)
        expected_distance = (self.target - self.source).length_squared()
        distance = (self.position - self.source).length_squared()

        if distance >= expected_distance:
            self.position = self.target.copy()
            self.source = self.target.copy()
        
            self.direction = pygame.Vector2(0, 0)

            if self.path.is_empty():
                self.__find_path()

            if self.path.is_empty():
                return

            i, j = self.path.take()
            
            self.target = pygame.Vector2(j * self.size.x, i * self.size.y)
            self.direction = self.target - self.source
            if self.direction.length_squared() > 1:
                self.direction.normalize_ip()
        
        self.update_animation()

