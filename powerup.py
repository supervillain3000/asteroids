import pygame
import random
from circleshape import CircleShape

class PowerUp(CircleShape):
    def __init__(self, x, y, radius=10):
        super().__init__(x, y, radius)
        self.power_up_timer = 10

    def apply_effect(self, player):
        """To be overridden by subclasses"""
        pass

    def update(self, dt):
        self.power_up_timer -= dt

class ShieldPowerUp(PowerUp):
    def __init__(self, x, y, radius=50):
        super().__init__(x, y, radius)
        self.image = pygame.image.load("assets/shield_powerup.png")
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))

    def draw(self, screen):
        screen.blit(self.image, (self.position.x - self.radius, self.position.y - self.radius))

    def apply_effect(self, player):
        """Give the player a temporary shield"""
        player.shield_active = True
        player.shield_timer = 5  # Shield lasts 5 seconds

class SpeedPowerUp(PowerUp):
    def __init__(self, x, y, radius=50):
        super().__init__(x, y, radius)
        self.image = pygame.image.load("assets/speed_powerup.png")
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))

    def draw(self, screen):
        screen.blit(self.image, (self.position.x - self.radius, self.position.y - self.radius))

    def apply_effect(self, player):
        """Increase player speed temporarily"""
        player.speed_boost = True
        player.speed_timer = 5
