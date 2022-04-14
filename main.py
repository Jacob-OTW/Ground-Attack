import pygame
import sys
import time
import math

from settings import *

from player_obj import player_group, play
from flare_obj import flare_group, Flare
from projectiles import projectile_group, Bomb
from vehicle_obj import vehicle_group, enemy_projectile_group
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
            if event.key == pygame.K_v:
                flare_group.add(Flare(play.local_pos((-40, 0)), play.going_right, play))


score_font = pygame.font.SysFont("arial", 32, pygame.font.Font.bold)


def main():
    last_time = time.time()
    while True:
        frame_time = time.time() - last_time
        last_time = time.time()
        # Update
        player_group.update()
        projectile_group.update()
        enemy_projectile_group.update()
        vehicle_group.update()
        effect_group.update()
        flare_group.update()
        HandleKeys()

        # Visual
        screen.fill((97, 201, 207))
        projectile_group.draw(screen)
        enemy_projectile_group.draw(screen)
        vehicle_group.draw(screen)
        player_group.draw(screen)
        flare_group.draw(screen)
        effect_group.draw(screen)

        text2 = score_font.render(f"{round(frame_time * 1000)}ms :: {len(effect_group.sprites())}", True, (255, 255, 255))
        screen.blit(text2, (100, 150))

        # Refresh
        pygame.display.flip()
        clock.tick(60)


main()
