import pygame


class Dot:
    def __init__(self, x, y, defs):
        self.position = pygame.Vector2(x, y)
        self.radius = defs['radius']
        self.on_collide = defs['on_collide']
        self.eaten = False
    
    def get_collision_rect(self):
        return pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2, self.radius * 2)

    def render(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), self.position, self.radius)
