import pygame

from .BaseEntity import BaseEntity, Direction


class Pacman(BaseEntity):
    def __init__(self, x, y, w, h, speed, texture, frames, interval, scene):
        animations = {
            (-1, 0): frames[0],
            (0, 1): frames[1],
            (1, 0): frames[2],
            (0, -1): frames[3],
        }
        super().__init__(x, y, w, h, speed, texture, interval, animations)
        self.current_animation = [frames[0][0]]
        self.scene = scene
        self.action_map = [self.request_left, self.request_down, self.request_right, self.request_up, self.do_nothing]
        self.score = 0
    
    def request_left(self):
        dir_num = self.dir_to_num()

        if dir_num == Direction.LEFT:
            # it is already moving to the left, there is no direction change
            return False

        if dir_num in [Direction.UP, Direction.DOWN, Direction.IDLE]:
            # Check if it is allowed to turn left
            # Get the center of pacman
            rect = self.get_collision_rect()
            cx, cy = rect.center
            ci, cj = int(cy // rect.height), int(cx // rect.width)
            if self.scene.map.charmap[ci][cj - 1] == '#':
                # There is wall to the left, it is not allowed to turn left.
                return False

            # Fix vertical position
            self.position.y = (cy // rect.height) * rect.height
        
        self.direction = pygame.Vector2(-1, 0)
        self.update_animation()
        return True
    
    def request_down(self):
        dir_num = self.dir_to_num()

        if dir_num == Direction.DOWN:
            # it is already moving down, there is no direction change
            return False

        if dir_num in [Direction.LEFT, Direction.RIGHT, Direction.IDLE]:
            # Check if it is allowed to turn down
            # Get the center of pacman
            rect = self.get_collision_rect()
            cx, cy = rect.center
            ci, cj = int(cy // rect.height), int(cx // rect.width)
            if self.scene.map.charmap[ci + 1][cj] == '#':
                # There is wall on bottom, it is not allowed to turn down.
                return False
        
            # Fix horizontal position
            self.position.x = (cx // rect.width) * rect.width

        self.direction = pygame.Vector2(0, 1)
        self.update_animation()
        return True
    
    def request_right(self):
        dir_num = self.dir_to_num()

        if dir_num == Direction.RIGHT:
            # it is already moving to the right, there is no direction change
            return False

        if dir_num in [Direction.UP, Direction.DOWN, Direction.IDLE]:
            # Check if it is allowed to turn right
            # Get the center of pacman
            rect = self.get_collision_rect()
            cx, cy = rect.center
            ci, cj = int(cy // rect.height), int(cx // rect.width)
            if self.scene.map.charmap[ci][cj + 1] == '#':
                # There is wall to the right, it is not allowed to turn right.
                return False
            
            # Fix vertical position
            self.position.y = (cy // rect.height) * rect.height

        self.direction = pygame.Vector2(1, 0)
        self.update_animation()
        return True
    
    def request_up(self):
        dir_num = self.dir_to_num()

        if dir_num == Direction.UP:
            # it is already moving up, there is no direction change
            return False

        if dir_num in [Direction.LEFT, Direction.RIGHT, Direction.IDLE]:
            # Check if it is allowed to turn up
            # Get the center of pacman
            rect = self.get_collision_rect()
            cx, cy = rect.center
            ci, cj = int(cy // rect.height), int(cx // rect.width)
            if self.scene.map.charmap[ci - 1][cj] == '#':
                # There is wall on top, it is not allowed to turn up.
                return False

            # Fix horizontal position
            self.position.x = (cx // rect.width) * rect.width

        self.direction = pygame.Vector2(0, -1)
        self.update_animation()
        return True

    def do_nothing(self):
        return self.dir_to_num() != Direction.IDLE

    def apply_action(self, action):
        self.action_map[action]()
    
    def update(self, dt):
        super().update(dt)

        # Fix pacman position
        rect = self.get_collision_rect()
        cx, cy = rect.center
        ci, cj = int(cy // rect.height), int(cx // rect.width)
        
        top_i = int(rect.top // rect.height)
        bottom_i = int(rect.bottom // rect.height)

        if '#' in (self.scene.map.charmap[top_i][cj], self.scene.map.charmap[bottom_i][cj]):
            # Collision with a top or a bottom wall
            self.position.y = (cy // rect.height) * rect.height

        left_j = int(rect.left // rect.width)
        right_j = int(rect.right // rect.width)

        if '#' in (self.scene.map.charmap[ci][left_j], self.scene.map.charmap[ci][right_j]):
            # Collision with a left or a right wall
            self.position.x = (cx // rect.width) * rect.width
        

        

