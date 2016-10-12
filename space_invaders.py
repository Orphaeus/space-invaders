import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from ship import Ship
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and create a screen object
    pygame.init()
    si_settings = Settings()
    screen = pygame.display.set_mode((si_settings.screen_width, si_settings.screen_height))
    pygame.display.set_caption('Space Invaders')

    # Create an instance to store game statistics
    stats = GameStats(si_settings)

    # Make a ship, a group to store bullets in, and a group to store aliens in
    ship = Ship(si_settings, screen)
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens
    gf.create_fleet(si_settings, screen, ship, aliens)

    # Start the main loop for the game
    while True:
        gf.check_events(si_settings, screen, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(si_settings, screen, ship, aliens, bullets)
            gf.update_aliens(si_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(si_settings, screen, ship, bullets, aliens)

run_game()
