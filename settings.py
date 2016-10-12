class Settings:
    # A class to store all settings for Space Invaders

    def __init__(self):
        # Initialize the game's settings

        # SCREEN SETTINGS
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (150, 150, 150)

        # SHIP SETTINGS
        self.ship_speed_factor = 1.25
        self.ship_limit = 3

        # BULLET SETTINGS
        self.bullet_speed_factor = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 200, 0
        self.bullets_allowed = 3

        # ALIEN SETTINGS
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # Fleet direction of 1 = right, -1 = left
        self.fleet_direction = 1
