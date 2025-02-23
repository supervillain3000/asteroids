import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from shot import Shot

def main():
    print(f"Starting Asteroids!\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    fps = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(x, y)
    asteroids_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill((0, 0, 0))

        for drawable_object in drawable:
            drawable_object.draw(screen)

        for updatable_object in updatable:
            updatable_object.update(dt)

        for asteroid in asteroids:
            if asteroid.check_collision(player):
                print("Game Over!")
                sys.exit(1)

        for asteroid in asteroids:
            for bullet in shots:
                if asteroid.check_collision(bullet):
                    asteroid.split()
                    bullet.kill()
            

        pygame.display.flip()
        dt = fps.tick(60) / 1000

if __name__ == "__main__":
    main()
