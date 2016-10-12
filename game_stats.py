class GameStats():
    # Track statistics for Space Invaders

    def __init__(self, si_settings):
        # Initialize statistics
        self.si_settings = si_settings
        self.reset_stats()

        # Start Space Invaders in an active state
        self.game_active = True

    def reset_stats(self):
        # Initialize stats that change during the game
        self.ships_left = self.si_settings.ship_limit
