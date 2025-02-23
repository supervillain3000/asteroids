import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN
from shot import Shot
from powerup import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.score = 0
        self.lives = 3
        self.invincible = False
        self.invincibility_timer = 0
        self.blink_timer = 0
        self.visible = True

        # Power-up effects
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost = False
        self.speed_timer = 0

        # Load the sprite image
        self.original_image = pygame.image.load("assets/player.png")
        self.original_image = pygame.transform.scale(self.original_image, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
        self.image = self.original_image

        self.shield_image = pygame.image.load("assets/shield_effect.png")  # Add a shield image
        self.shield_image = pygame.transform.scale(self.shield_image, (PLAYER_RADIUS * 2.5, PLAYER_RADIUS * 2.5))

    def draw(self, screen):
        if self.shield_active:
            shield_rect = self.shield_image.get_rect(center=(self.position.x, self.position.y))
            screen.blit(self.shield_image, shield_rect.topleft)
        if self.visible:  
            # Rotate the image, adjusting for the default sprite direction
            rotated_image = pygame.transform.rotate(self.original_image, -self.rotation + 180)  
            rect = rotated_image.get_rect(center=(self.position.x, self.position.y))
            screen.blit(rotated_image, rect.topleft)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):

        # Handle invincibility blinking
        if self.invincible:
            self.invincibility_timer -= dt
            self.blink_timer += dt
            if self.blink_timer >= 0.2:
                self.visible = not self.visible
                self.blink_timer = 0  
            if self.invincibility_timer <= 0:
                self.invincible = False
                self.visible = True

        # Handle shield power-up
        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False
                self.invincible = False  # Shield wears off

        # Handle speed boost power-up
        if self.speed_boost:
            self.speed_timer -= dt
            if self.speed_timer <= 0:
                self.speed_boost = False

        keys = pygame.key.get_pressed()

        if self.timer > 0:
            self.timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()

        keys = pygame.key.get_pressed()

        if self.timer > 0:
            self.timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)
        
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        speed = PLAYER_SPEED * 1.5 if self.speed_boost else PLAYER_SPEED  # Increase speed if boosted
        self.position += forward * speed * dt

    def apply_powerup(self, powerup):
        if isinstance(powerup, ShieldPowerUp):
            self.shield_active = True
            self.invincible = True  # Player becomes invincible
            self.shield_timer = 5  # Shield lasts 5 seconds

        elif isinstance(powerup, SpeedPowerUp):
            self.speed_boost = True
            self.speed_timer = 5  # Speed boost lasts 5 seconds


    def shoot(self):
        vector = pygame.Vector2(0, 1) * PLAYER_SHOOT_SPEED  # Adjusting for correct direction
        velocity = vector.rotate(self.rotation)  # Rotate bullet in the direction of the ship
        shot = Shot(self.position.x, self.position.y, velocity)  # Pass velocity correctly
        self.timer = PLAYER_SHOOT_COOLDOWN