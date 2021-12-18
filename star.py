import pygame
from pygame.sprite import Sprite

from random import randint


class Star(Sprite):
    def __init__(self, ai_settings, screen):
        super(Star, self).__init__()
        self.screen = screen

        self.image = pygame.image.load("images/star.bmp")
        self.rect = self.image.get_rect()

        # every new alien spawns in top left position
        self.rect.x = randint(0, ai_settings.screen_width)
        self.rect.y = randint(0, ai_settings.screen_height)

        # # star spawn in random position.
        # self.position_x = randint(16, ai_settings.screen_width - 16)
        # self.position_y = randint(16, ai_settings.screen_height - 16)
