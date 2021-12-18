import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    ai_settings = Settings()
    
    screen = pygame.display.set_mode((
        ai_settings.screen_width,
        ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")

    # Создание кнопки Play
    play_button = Button(ai_settings, screen, "Play")

    # Создание корабля
    ship = Ship(screen, ai_settings)

    # Создание группы для хранения пуль
    bullets = Group()

    # Создание групы для пришельцев
    aliens = Group()

    # Создание групы для звезд
    stars = Group()

    # Создание звезд
    gf.create_stars(ai_settings, screen, stars)

    # Создание флота пришельцев.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Создание экземпляра для хранения игровой статистики.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Запуск основного цикла игры
    while True:
        gf.check_events(ai_settings, screen, stats,
                        play_button, ship, aliens, bullets, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, ship,
                              aliens, bullets, sb)
            gf.update_aliens(ai_settings, stats, screen,
                             ship, aliens, bullets, sb)
        gf.update_screen(ai_settings, screen, stats,
                             ship, aliens, bullets,
                             play_button, stars, sb)


if __name__ == "__main__":
    run_game()
