import pygame
import math

SCREEN_WIDTH = 1230
SCREEN_HEIGHT = 930
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
SCORE = 0
LIVES = 3

Convert = 360 / math.pi*2
