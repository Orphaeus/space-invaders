import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_events(si_settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, si_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, si_settings, screen, ship, bullets):
    # Respond to keypresses
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame. K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            fire_bullet(si_settings, screen, ship, bullets)
        elif event.key == pygame.K_q:
            sys.exit()


def check_keyup_events(event, ship):
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False


def update_screen(si_settings, screen, ship, bullets, aliens):
    # Redraw the screen during each pass through the loop
    screen.fill(si_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(si_settings, screen, ship, aliens, bullets):
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(si_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(si_settings, screen, ship, aliens, bullets):
    # Check for bullet/alien collisions and remove any relevant bullets and aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Destroy existing bullets and create a new fleet
        bullets.empty()
        create_fleet(si_settings, screen, ship, aliens)


def fire_bullet(si_settings, screen, ship, bullets):
    # Create a new bullet and add it to the bullets group
    if len(bullets) < si_settings.bullets_allowed:
        new_bullet = Bullet(si_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_of_aliens_x(si_settings, alien_width):
    # Determine the number of aliens that fit in a row
    available_space_x = si_settings.screen_width - 4 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(si_settings, ship_height, alien_height):
    # Determine the number of rows of aliens that fit on the screen
    available_space_y = (si_settings.screen_height - (7 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(si_settings, screen, aliens, alien_number, row_number):
    # Create an alien and place it in the row
    alien = Alien(si_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(si_settings, screen, ship, aliens):
    # Create a fleet of aliens

    # Create an alien and find the number of aliens in a row
    # Spacing between aliens is equal to one alien width
    alien = Alien(si_settings, screen)
    number_aliens_x = get_number_of_aliens_x(si_settings, alien.rect.width)
    number_rows = get_number_rows(si_settings, ship.rect.height, alien.rect.height)

    # Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(si_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(si_settings, aliens):
    # Respond appropriately if any aliens have reached an edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(si_settings, aliens)
            break


def check_aliens_bottom(si_settings, stats, screen, ship, aliens, bullets):
    # Check if any aliens have reached the bottom of the screen
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(si_settings, stats, screen, ship, aliens, bullets)
            break


def change_fleet_direction(si_settings, aliens):
    # Drop the fleet and change direction
    for alien in aliens.sprites():
        alien.rect.y += si_settings.fleet_drop_speed
    si_settings.fleet_direction *= -1


def update_aliens(si_settings, stats, screen, ship, aliens, bullets):
    # Check if fleet is at an edge, then update fleet positions
    check_fleet_edges(si_settings, aliens)
    aliens.update()
    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(si_settings, stats, screen, ship, aliens, bullets)

    # Look for alien/ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(si_settings, stats, screen, ship, aliens, bullets)


def ship_hit(si_settings, stats, screen, ship, aliens, bullets):
    # Respond to ship being hit by aliens

    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        
        # Pause
        sleep(0.5)
        # Create a new fleet and center the ship
        create_fleet(si_settings, screen, ship, aliens)
        ship.center_ship()

    else:
        stats.game_active = False
