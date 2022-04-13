import pygame
import sys
import time
import math

from settings import *

from player_obj import player_group, play
from projectiles import projectile_group, Bomb
from vehicle_obj import vehicle_group
from effects import effect_group


def HandleKeys():
    if LIVES <= 0:
        pygame.quit()
        print(SCORE)
        sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                projectile_group.add(Bomb(play.rect.center, play.angle, play.going_right))


score_font = pygame.font.SysFont("arial", 32, pygame.font.Font.bold)


def main():
    last_time = time.time()
    while True:
        frame_time = time.time() - last_time
        last_time = time.time()
        # Update
        player_group.update()
        projectile_group.update()
        vehicle_group.update()
        effect_group.update()
        HandleKeys()

        # Visual
        screen.fill((97, 201, 207))
        projectile_group.draw(screen)
        vehicle_group.draw(screen)
        effect_group.draw(screen)
        player_group.draw(screen)

        text2 = score_font.render(f"{len(projectile_group.sprites())}", True, (255, 255, 255))
        screen.blit(text2, (100, 150))

        # Refresh
        pygame.display.flip()
        clock.tick(60)


main()
