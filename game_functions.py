import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien
from star import Star


def check_keydown_events(event, ai_settings, screen,
                         ship, bullets, stats, aliens, sb):
    """Реагирует на нажатия клавиш."""
    if event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_w:
        ship.moving_up = True
    elif event.key == pygame.K_s:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats,
                   ship, aliens, bullets, sb)
    elif event.key == pygame.K_BACKSPACE:
        sys.exit()


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""
    if event.key == pygame.K_d:
        ship.moving_right = False
    if event.key == pygame.K_a:
        ship.moving_left = False
    if event.key == pygame.K_w:
        ship.moving_up = False
    if event.key == pygame.K_s:
        ship.moving_down = False


def check_events(ai_settings, screen, stats,
                 play_button, ship, aliens, bullets, sb):
    """Обрабатывает нажатия клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen,
                                 ship, bullets, stats, aliens, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats,
                              play_button, ship, aliens,
                              bullets, mouse_x, mouse_y, sb)


def check_play_button(ai_settings, screen, stats,
                      play_button, ship, aliens,
                      bullets, mouse_x, mouse_y, sb):
    """Запускает новую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats,
                   ship, aliens, bullets, sb)


def start_game(ai_settings, screen, stats,
               ship, aliens, bullets, sb):
    ai_settings.initialize_dynamic_settings()
    # Указатель мыши скрывается.
    pygame.mouse.set_visible(False)
    # Сброс игровой статистики.
    stats.reset_stats()

    stats.game_active = True

    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Очистка списков пришельцев и пуль.
    aliens.empty()
    bullets.empty()

    # Создание нового флота и размещение корабля в црентре.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def update_screen(ai_settings, screen, stats,
                  ship, aliens, bullets,
                  play_button, stars, sb):

    screen.fill(ai_settings.bg_color)
    stars.draw(screen)

    # Все пули вывлдятся позади изображений корабля и пришельцев.
    for bullet in bullets.sprites():
        if len(bullets) < ai_settings.bullets_allowed:
            bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Вывод счета.
    sb.show_score()

    # Кнопка Play отображаеться в том случае, если игра неактивна.
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего прорисованного экрана.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, ship,
                   aliens, bullets, sb):
    """Обновляет позици пуль и удаляет старые пули."""

    # Обновляет позицци пуль
    bullets.update()

    # Удаление пуль, вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Проверка попаданий пуль в пришельцев.

    check_bullet_alien_collisions(ai_settings, screen, stats, ship,
                                  aliens, bullets, sb)


def check_bullet_alien_collisions(ai_settings, screen, stats, ship,
                                  aliens, bullets, sb):
    """Обработка коллизий пуль с пришельцами."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
    sb.prep_score()
    check_high_score(stats, sb)
    # Удаление пуль и пришельцев, участвующих в коллизиях.
    if len(aliens) == 0:
        # Уничтожение существующих пуль и создание нового флота.
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум еще не достингут."""
    # Создание новой пули и включение ее в группу bullets.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещяющихся на экране."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) -
                         ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens,
                 alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien_height + 2 * alien_height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот прлишельцев."""
    # Создание пришельца и вычисление количнства пришельцев в ряду.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Создание первого ряда пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Реагирет на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen,
                  ship, aliens, bullets, sb):
    """
    Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Проверка коллизий "пришелец - корабль".
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)

    # Проверка пришельцев, добравшихся до нижнего края экрана.
    check_aliens_bottom(ai_settings, stats, screen,
                        ship, aliens, bullets, sb)


def create_stars(ai_settings, screen, stars):
    for number in range(ai_settings.number_of_stars):
        star = Star(ai_settings, screen)
        stars.add(star)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Обрабатывает столкновение корябля с пришельцем."""
    if stats.ships_left > 0:

        # Уменьшение ships_left.
        stats.ships_left -= 1

        sb.prep_ships()

        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen,
                        ship, aliens, bullets, sb):
    """Проперяет, добрались ли пришельцы до нижнего края экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что при столкновении с кораблем.
            ship_hit(ai_settings, stats, screen,
                     ship, aliens, bullets, sb)
            break


def check_high_score(stats, sb):
    "Проверяет, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
