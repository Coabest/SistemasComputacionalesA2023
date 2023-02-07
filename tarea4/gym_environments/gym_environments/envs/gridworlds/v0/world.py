import pygame
import pathlib
import time
import numpy as np
from . import settingss
from .tilemap import TileMap


class World:
    def __init__(self, title, state, action, P, battery):
        pygame.init()
        pygame.display.init()
        pygame.mixer.music.load(settingss.BASE_DIR / "assets" / "sounds" / "retro_music.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        self.render_surface = pygame.Surface(
            (settingss.VIRTUAL_WIDTH, settingss.VIRTUAL_HEIGHT)
        )
        self.screen = pygame.display.set_mode(
            (settingss.WINDOW_WIDTH, settingss.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(title)
        self.battery = battery
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
        tile_texture_names = ["floor" for _ in range(settingss.NUM_TILES)]
        self.tilemap = TileMap(tile_texture_names, np.random.randint(0,settingss.FLOOR_FRAMES))

    def reset(self, state, action):
        self.state = state
        self.action = action
        self.render_character = True
        self.render_goal = True

    def update(self, battery, state, action, reward, terminated):
        if terminated:
            if state == self.finish_state:
                self.render_goal = False
                settingss.SOUNDS['power_up'].play()
            else:
                self.render_character = True
                pygame.mixer.music.set_volume(0.1)
                settingss.SOUNDS['power_down'].play()
                time.sleep(1)
                pygame.mixer.music.set_volume(0.5)

        self.battery = battery
        self.state = state
        self.action = action

    def render(self):
        self.render_surface.fill((0, 0, 0))

        self.tilemap.render(self.render_surface)

        if self.render_goal:
            self.render_surface.blit(
                 settingss.TEXTURES['checkpoint'],
                (self.tilemap.tiles[self.finish_state].x,
                 self.tilemap.tiles[self.finish_state].y)
            )

        if self.render_character:
            battery_slice = max(0, int(np.ceil(self.battery * settingss.ROBOT_FRAMES / settingss.BATTERY)) )
            self.render_surface.blit(
                 settingss.TEXTURES['robot'][battery_slice],
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
