"""
ISPTSC 2023
Lecture 1

Author: Alejandro Mujica - alejandro.j.mujic4@gmail.com
Author: Jesús Pérez - perezj89@gmail.com
AUthor: Coalbert Ramirez - coabest15@gmail.com

This file contains the the Two-Armed Bandit Environment.
"""
import time

import gym

import numpy as np

import pygame

from . import settings

pygame.init()
pygame.display.init()


class Arm:
    def __init__(self, p=0, earn=0):
        self.probability = p
        self.earn = earn
    
    def pull(self):
        return self.earn if np.random.random() < self.probability else 0

    def __str__(self):
        return f"Arm: p = {self.probability}, earn: {self.earn}"
    
    def __repr__(self):
        return f"Arm: p = {self.probability}, earn: {self.earn}"


class TwoArmedBanditEnv(gym.Env):
    
    def __init__(self):
        self.arms = (
            Arm(0.5, 1),
            Arm(0.1, 100)
        )
        self.counter = 0
        self.total_reward = 0
        self.action = None
        self.reward = None
        self.observation_space = gym.spaces.Discrete(1)
        self.action_space = gym.spaces.Discrete(len(self.arms))

        self.window = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Two-Armed Bandit Environment")        

    def _get_observations(self):
        return 0

    def _get_info(self):
        return { 'state': 0 }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        return self._get_observations(), self._get_info()

    def step(self, action):
        self.action = action
        self.reward = self.arms[action].pull()
        self.render()
        return self._get_observations(), self.reward, False, False, self._get_info()

    def render(self):

        # Arrows and reward text's coordinates
        y = settings.WINDOW_HEIGHT - 50 - settings.ARROW_HEIGHT / 2
        x = 50 + settings.MACHINE_WIDTH / 2
        dir = 1

        if self.action == 1:
            x += settings.MACHINE_WIDTH + 50
            dir = -1

        animation_lenght = 20
        for _ in range (animation_lenght):
            self.window.fill((255, 100, 100))

            # Render the first machine
            self.window.blit(settings.TEXTURES['machine'], (50, 100))

            # Render the second machine
            self.window.blit(
                settings.TEXTURES['machine'],
                (100 + settings.MACHINE_WIDTH,
                 100))

            # Render the arrow under the selected machine
            self.window.blit(
                settings.TEXTURES['arrow'], (x - settings.ARROW_WIDTH / 2 - 80, y))

            # Render the reward
            text_reward = settings.FONTS['font'].render(
                f"{self.reward}",
                True,
                (235 + self.counter,
                 180 - self.counter * 3,
                 self.counter * 4))
            text_rect = text_reward.get_rect()
            text_rect.center = (x, 110)

            self.window.blit(
                text_reward,
                (text_rect.x + self.counter * dir * 8,
                 text_rect.y - self.counter * 2))
            self.counter = (self.counter + 1)%animation_lenght

            # Add reward to total
            if self.counter == animation_lenght - 2:
                self.total_reward += self.reward

            # Render total reward
            text_reward = settings.FONTS['font'].render(
                f"{self.total_reward}", True, (235, 180, 0))
            text_total_rect = text_reward.get_rect()
            text_total_rect.center = (settings.WINDOW_WIDTH/2, 70)
            self.window.blit(text_reward, text_total_rect)

            pygame.event.pump()
            pygame.display.update()

            time.sleep(0.01)
     
    def close(self):
        pygame.display.quit()
        pygame.font.quit()
        pygame.quit()

