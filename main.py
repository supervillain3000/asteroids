import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid, Explosion
from asteroidfield import AsteroidField
from circleshape import CircleShape
from shot import Shot
from powerup import *

updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()

def main():
    print(f"Starting Asteroids!\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    background = pygame.image.load("assets/background.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    fps = pygame.time.Clock()
    dt = 0


    pygame.font.init()
    font = pygame.font.Font(None, 36)

    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    PowerUp.containers = (powerups, drawable, updatable)

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Explosion.containers = updatable, drawable
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(x, y)
    asteroids_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        screen.blit(background, (0, 0))

        for drawable_object in drawable:
            if isinstance(drawable_object, Player) and not drawable_object.visible:
                continue
            drawable_object.draw(screen)

        for updatable_object in updatable:
            updatable_object.update(dt)

        if not player.invincible:
            for asteroid in asteroids:
                if asteroid.check_collision(player):
                    if player.lives <= 0:
                        print("Game Over!")
                        sys.exit(1)
                    if player.shield_active:
                        player.shield_active = False
                        player.invincible = True
                        player.invincibility_timer = 2 
                    else: 
                        player.lives -= 1
                        player.invincible = True
                        player.invincibility_timer = 2 

        for asteroid in asteroids:
            for bullet in shots:
                if asteroid.check_collision(bullet):
                    asteroid.split()
                    bullet.kill()
                    player.score += 1

        for powerup in powerups:
            if powerup.check_collision(player):
                powerup.apply_effect(player)
                powerup.kill()
            if powerup.power_up_timer <= 0:
                powerup.kill()
            

        score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 40))

        pygame.display.flip()
        dt = fps.tick(60) / 1000

if __name__ == "__main__":
    main()
