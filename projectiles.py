import pygame
import math
import random

from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/bullet.png'), angle - 90, 0.1)
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


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, angle, r: bool):
        super().__init__()
        self.angle = angle
        self.pos = pos
        self.going_right = r
        self.stored = pygame.transform.rotozoom(pygame.image.load('Assets/bomb.png').convert_alpha(), 0, 0.4)
        self.image = pygame.transform.rotate(self.stored, self.angle - 90)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        con = (360 / (math.pi * 2))
        self.pos += pygame.math.Vector2((3*math.sin(self.angle / con), 3*math.cos(self.angle / con)))
        if self.going_right:
            if self.angle > 0:
                self.angle -= 0.3
        else:
            if self.angle < 360:
                self.angle += 0.3
        self.image = pygame.transform.rotate(self.stored, self.angle - 90)
        self.rect = self.image.get_rect(center=self.pos)


projectile_group = pygame.sprite.Group()
