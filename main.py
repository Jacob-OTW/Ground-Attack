import math

import pygame
import sys
import time

from settings import *

from player_obj import player_group, play


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
            if event.key == pygame.K_e:
                pass


score_font = pygame.font.SysFont("arial", 32, pygame.font.Font.bold)


def main():
    last_time = time.time()
    while True:
        frame_time = time.time() - last_time
        last_time = time.time()
        # Update
        player_group.update()
        HandleKeys()

        # Visual
        screen.fill((97, 201, 207))
        player_group.draw(screen)

        text2 = score_font.render(f"a:{round(play.angle)} cos:{math.cos(play.angle / (360 / math.pi * 2))}", True, (255, 255, 255))
        screen.blit(text2, (100, 150))

        # Refresh
        pygame.display.flip()
        clock.tick(60)


main()
