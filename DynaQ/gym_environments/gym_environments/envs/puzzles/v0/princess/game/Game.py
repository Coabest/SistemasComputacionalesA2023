import pygame

from .src.World import World


class Game:
    def __init__(self, title, render_mode):
        self.render_mode = render_mode

        self.world = World()

        if self.render_mode is not None:
            pygame.init()
            pygame.display.init()

            w, h = self.world.tile_map.width, self.world.tile_map.height

            self.render_surface = pygame.Surface((w, h))
            self.screen = pygame.display.set_mode((w * 4, h * 4))
            pygame.display.set_caption(title)

    def reset(self):
        return self.world.reset()

    def get_state(self):
        return self.world.get_state()

    def update(self, action):
        return self.world.apply_action(action)

    def render(self):
        if self.render_mode is None:
            return

        self.render_surface.fill((0, 0, 0))

        self.world.render(self.render_surface)

        self.screen.blit(
            pygame.transform.scale(self.render_surface, self.screen.get_size()), (0, 0)
        )

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        pygame.display.quit()
        pygame.quit()
