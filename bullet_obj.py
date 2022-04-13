import pygame
import math
import random

from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/bullet.png'), angle, 0.1)
        self.image.fill('Black')
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.mask = pygame.mask.from_surface(self.image)
        angle += random.uniform(-3, 3)
        con = 360 / (math.pi * 2)
        x = 20 * math.sin(angle / con)
        y = 20 * math.cos(angle / con)
        self.vec = pygame.math.Vector2((x, y))

    def update(self):
        self.pos += self.vec
        self.rect.center = self.pos
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()


bullet_group = pygame.sprite.Group()
