import pygame

from .src.Scene import Scene
from . import settings


class Game:
    def __init__(self, title, render_mode):
        self.render_mode = render_mode

        self.scene = Scene()

        if self.render_mode is not None:
            pygame.init()
            pygame.display.init()

            self.render_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
            self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
            pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()


    def reset(self):
        return self.scene.reset()

    def get_state(self):
        return self.scene.get_state()

    def update(self, action, fps):
        self.scene.apply_action(action)

        dt = self.clock.tick(fps) / 1000.0

        effective_action = self.scene.update(dt)
        
        new_state = self.get_state()
        win = self.scene.check_win()
        lose = self.scene.check_lose()
        return new_state, win, lose, effective_action

    def render(self):
        if self.render_mode is None:
            return

        self.render_surface.fill((0, 0, 0))

        self.scene.render(self.render_surface)

        self.screen.blit(
            pygame.transform.scale(self.render_surface, self.screen.get_size()), (0, 0)
        )

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        if self.render_mode is None:
            return

        pygame.display.quit()
        pygame.quit()
