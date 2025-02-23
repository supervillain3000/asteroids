import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_MIN_SPLIT_ANGLE, ASTEROID_MAX_SPLIT_ANGLE, ASTEROID_SPLITTED_VELOCITY_MULTIPLIER

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(ASTEROID_MIN_SPLIT_ANGLE, ASTEROID_MAX_SPLIT_ANGLE)
    
        splitted_asteroid_1 = Asteroid(self.position.x, self.position.y, (self.radius - ASTEROID_MIN_RADIUS ))
        splitted_asteroid_2 = Asteroid(self.position.x, self.position.y, (self.radius - ASTEROID_MIN_RADIUS ))
        
        splitted_asteroid_1.velocity = self.velocity.rotate(random_angle) * ASTEROID_SPLITTED_VELOCITY_MULTIPLIER
        splitted_asteroid_2.velocity = self.velocity.rotate(-random_angle) * ASTEROID_SPLITTED_VELOCITY_MULTIPLIER
        