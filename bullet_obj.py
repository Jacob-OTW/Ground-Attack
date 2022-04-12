import pygame
import math
import random


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/bullet.png'), angle, 0.1)
        self.pos = pos
        angle += random.uniform(-3, 3)
        con = 360 / (math.pi * 2)
        x = 10 * math.sin(angle / con)
        y = 10 * math.cos(angle / con)
        self.vec = pygame.math.Vector2((x, y))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.pos += self.vec
        self.rect.center = self.pos


bullet_group = pygame.sprite.Group()
