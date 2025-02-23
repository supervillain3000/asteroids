import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, SHOT_RADIUS)

        # Load and scale bullet image
        self.original_image = pygame.image.load("assets/bullets.png")
        self.image = pygame.transform.scale(self.original_image, (SHOT_RADIUS * 2, SHOT_RADIUS * 2))

        # Rotate image based on velocity
        angle = velocity.angle_to(pygame.Vector2(1, 0))  
        self.image = pygame.transform.rotate(self.image, -angle)

        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = velocity  # Bullet movement speed

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = (self.position.x, self.position.y)  # Keep sprite aligned

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)