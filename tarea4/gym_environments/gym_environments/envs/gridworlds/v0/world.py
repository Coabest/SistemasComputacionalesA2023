import pygame

from . import settingss
from .tilemap import TileMap


class World:
    def __init__(self, title, state, action, P, battery):
        pygame.init()
        pygame.display.init()
        pygame.mixer.music.play(loops=-1)
        self.render_surface = pygame.Surface(
            (settingss.VIRTUAL_WIDTH, settingss.VIRTUAL_HEIGHT)
        )
        self.screen = pygame.display.set_mode(
            (settingss.WINDOW_WIDTH, settingss.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(title)
        self.current_state = state
        self.state = state
        self.current_action = action
        self.action = action
        self.render_character = True
        self.render_goal = True
        self.tilemap = None
        self.finish_state = settingss.FINAL_STATE
        self._create_tilemap()

    def _create_tilemap(self):
        tile_texture_names = ["ice" for _ in range(settingss.NUM_TILES)]
        self.tilemap = TileMap(tile_texture_names)

    def reset(self, state, action):
        self.state = state
        self.action = action
        self.render_character = True
        self.render_goal = True

    def update(self, state, action, reward, terminated):
        if terminated:
            if state == self.finish_state:
                self.render_goal = False
                settingss.SOUNDS['win'].play()
            else:
                self.tilemap.tiles[state].texture_name = "cracked_hole"
                self.render_character = False
                settingss.SOUNDS['ice_cracking'].play()
                settingss.SOUNDS['water_splash'].play()

        self.state = state
        self.action = action

    def render(self):
        self.render_surface.fill((0, 0, 0))

        self.tilemap.render(self.render_surface)

        self.render_surface.blit(
            settingss.TEXTURES['stool'],
            (self.tilemap.tiles[0].x, self.tilemap.tiles[0].y)
        )

        if self.render_goal:
            self.render_surface.blit(
                settingss.TEXTURES['goal'],
                (self.tilemap.tiles[self.finish_state].x,
                 self.tilemap.tiles[self.finish_state].y)
            )

        if self.render_character:
            self.render_surface.blit(
                # settingss.TEXTURES['character'][self.action],
                 settingss.TEXTURES['robot0'],
                (self.tilemap.tiles[self.state].x,
                 self.tilemap.tiles[self.state].y)
            )

        self.screen.blit(
            pygame.transform.scale(
                self.render_surface,
                self.screen.get_size()),
            (0, 0)
        )

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.display.quit()
        pygame.quit()
