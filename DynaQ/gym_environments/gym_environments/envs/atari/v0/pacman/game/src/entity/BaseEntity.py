import pygame

class Direction:
    LEFT = 0
    DOWN = 1
    RIGHT = 2
    UP = 3
    IDLE = 4


class BaseEntity:
    DIR_MAP = {
        (0, 0): Direction.IDLE,
        (-1, 0): Direction.LEFT,
        (0, 1): Direction.DOWN,
        (1, 0): Direction.RIGHT,
        (0, -1): Direction.UP
    }

    def __init__(self, x, y, w, h, speed, texture, interval, animations):
        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(w, h)
        self.direction = pygame.Vector2(0, 0)
        self.source = pygame.Vector2(x, y)
        self.target = pygame.Vector2(x, y)
        self.speed = speed
        self.texture = texture
        self.anim_interval = interval
        self.animations = animations
        self.current_animation = None
        self.current_frame = 0
        self.current_animation_time = 0

    def dir_to_num(self):
        return self.DIR_MAP[(int(self.direction.x), int(self.direction.y))]
    
    def get_collision_rect(self):
        return pygame.Rect(self.position, self.size)
    
    def update_animation(self):
        new_animation = self.animations.get((int(self.direction.x), int(self.direction.y)))
        
        if new_animation is None or new_animation == self.current_animation:
            return
        
        self.current_animation = new_animation
        self.current_frame = 1
        self.current_animation_time = 0
    
    def update(self, dt):
        if len(self.current_animation) > 1:
            self.current_animation_time += dt

            if self.current_animation_time >= self.anim_interval:
                self.current_animation_time = self.current_animation_time % self.anim_interval
                self.current_frame = (self.current_frame + 1) % len(self.current_animation)
        
        if self.direction.length_squared() == 0:
            return
        
        velocity = self.direction * self.speed
        self.position += velocity * dt
        
    def render(self, surface):
        surface.blit(self.texture, self.position, self.current_animation[self.current_frame])
