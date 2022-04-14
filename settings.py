import pygame
import math
import time

SCREEN_WIDTH = 1230
SCREEN_HEIGHT = 930
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
SCORE = 0
LIVES = 3


def dir_to(mp, tp):
    dx = tp[0] - mp[0]
    dy = tp[1] - mp[1]
    rads = math.atan2(-dy, dx)
    rads %= 2 * math.pi
    return math.degrees(rads)


def dis_to(mp, tp):
    return math.hypot(mp[0] - tp[0], mp[1] - tp[1])
