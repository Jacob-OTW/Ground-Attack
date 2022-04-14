import pygame
import math
import random

from settings import *
from effects import Explosion


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/bullet.png').convert_alpha(), angle, 0.1)
        self.image.fill('Black')
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.mask = pygame.mask.from_surface(self.image)
        angle += random.uniform(-3, 3)
        self.vec = pygame.math.Vector2((20, 0)).rotate(angle)

    def update(self):
        self.pos[0] += self.vec[0]
        self.pos[1] -= self.vec[1]
        self.rect.center = self.pos
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, angle, r: bool):
        super().__init__()
        self.angle = angle
        self.pos = pygame.math.Vector2(pos)
        self.going_right = r
        self.stored = pygame.transform.rotozoom(pygame.image.load('Assets/bomb.png').convert_alpha(), 0, 0.4)
        self.image = pygame.transform.rotate(self.stored, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.going_right:
            v = pygame.math.Vector2((3, 0)).rotate(self.angle)
            self.pos[0] += v[0]
            self.pos[1] -= v[1]
            if self.angle > -90 if self.angle < 0 else self.angle > 270 or self.angle < 90:
                self.angle -= 0.3
        else:
            v = pygame.math.Vector2((3, 0)).rotate(self.angle)
            self.pos[0] += v[0]
            self.pos[1] -= v[1]
            if self.angle <= 270:
                self.angle += 0.3
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.explode()
        self.image = pygame.transform.rotate(self.stored, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def explode(self):
        Explosion.add_explosion(self.rect.midbottom)
        self.kill()


projectile_group = pygame.sprite.Group()
