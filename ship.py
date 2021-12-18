import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, screen, ai_settings) -> None:
        """Init the ship and set the start position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Every new ship spawn in bottom center
        self.center = float(self.screen_rect.centerx)
        self.bottom = float(self.screen_rect.bottom)

        # Moving toggles
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship position by the toggle."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
            
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        if self.moving_up and self.rect.top > 0:
            self.bottom -= self.ai_settings.ship_speed_factor

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.ship_speed_factor

        # Обновление атрибута rect на основании self.center.
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def blitme(self):
        """Display ship in current position."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корябль в центре нижней стороны."""
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom
