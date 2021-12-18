class Settings:
    """Класс для ранения настроек игры Alien Invasion."""
    def __init__(self) -> None:
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (20, 0, 50)

        # Параметры корабля
        # self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Параметры пули
        # self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 40, 255, 40
        self.bullets_allowed = 6

        # Количество звезд на карте
        self.number_of_stars = 15

        # Настройки пришельцев
        # self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # self.fleet_direction = 1

        # Темп ускорения игры
        self.speedup_scale = 1.4
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Иницилизирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_points = 50

        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличение настройки скорости."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
