import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_MIN_SPLIT_ANGLE, ASTEROID_MAX_SPLIT_ANGLE, ASTEROID_SPLITTED_VELOCITY_MULTIPLIER
from powerup import *

class Asteroid(CircleShape):
    containers = None  # This will hold (asteroids, updatable, drawable)

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        # Load the asteroid image
        self.original_image = pygame.image.load("assets/asteroid.png")  
        self.original_image = pygame.transform.scale(self.original_image, (radius * 2, radius * 2))
        self.image = self.original_image  

        # Automatically add itself to the correct sprite groups
        if Asteroid.containers:
            asteroids, updatable, drawable = Asteroid.containers
            asteroids.add(self)
            updatable.add(self)
            drawable.add(self)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, self.velocity.angle_to(pygame.Vector2(1, 0)))
        rect = rotated_image.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_image, rect.topleft)
    
    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()  # Remove this asteroid

        if Asteroid.containers:
            _, updatable, drawable = Asteroid.containers

            # Create explosion
            explosion = Explosion(self.position.x, self.position.y, self.radius * 2)
            updatable.add(explosion)
            drawable.add(explosion)

        if random.random() < 0.2:  # 20% chance to spawn a power-up
            powerup_type = random.choice([ShieldPowerUp, SpeedPowerUp])
            powerup = powerup_type(self.position.x, self.position.y)
            updatable.add(powerup)
            drawable.add(powerup)


        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        random_angle = random.uniform(ASTEROID_MIN_SPLIT_ANGLE, ASTEROID_MAX_SPLIT_ANGLE)

        new_asteroid_1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        new_asteroid_2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)

        new_asteroid_1.velocity = self.velocity.rotate(random_angle) * ASTEROID_SPLITTED_VELOCITY_MULTIPLIER
        new_asteroid_2.velocity = self.velocity.rotate(-random_angle) * ASTEROID_SPLITTED_VELOCITY_MULTIPLIER


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()

        # Load explosion frames
        self.frames = [pygame.image.load(f"assets/explosions/explosion_{i}.png") for i in range(6)]
        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (size, size))
        self.rect = self.image.get_rect(center=(x, y))

        self.animation_speed = 0.1  # Adjust as needed
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.animation_speed:
            self.timer = 0
            self.current_frame += 1
            if self.current_frame < len(self.frames):
                self.image = pygame.transform.scale(self.frames[self.current_frame], (self.rect.width, self.rect.height))
            else:
                self.kill()  # Remove explosion when animation ends

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
