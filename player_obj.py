import pygame
import math

from settings import *
from bullet_obj import bullet_group, Bullet


def dir_to(mp, tp):
    x = tp[0] - mp[0]
    y = tp[1] - mp[1]
    if y == 0:
        return 90 if x > 0 else 270
    if y > 0:
        v = (math.atan(x / y)) * 57.29577951
    else:
        v = math.atan(x / y) * 57.29577951 + 180
    while v > 360 or v < 0:
        if v > 360:
            v -= 360
        if v < 0:
            v += 360
    return v


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.stored = pygame.transform.scale(pygame.image.load('Assets/plane.png.png').convert_alpha(), (100, 32))
        self.image = self.stored
        self.rect = self.image.get_rect(left=0, top=SCREEN_HEIGHT / 8)
        self.pos = self.rect
        self.going_right = True
        self.angle = 0
        self.speed = 4
        self.m = 0.0

    def update(self):
        self.move()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullet_group.add(Bullet(self.rect.center, self.angle))

    def move(self):
        if self.going_right:
            if self.rect.right >= SCREEN_WIDTH:
                self.going_right = False
                self.angle = 270
                self.stored = pygame.transform.flip(
                    pygame.transform.scale(pygame.image.load('Assets/plane.png.png').convert_alpha(), (100, 32)), False,
                    True)
            self.pos = (self.pos[0] + 2, self.pos[1])
            a = dir_to(self.rect.center, pygame.mouse.get_pos())
            if 10 < a < 170:
                self.angle = a
            else:
                self.angle = 90
            b = 2 * math.cos(self.angle / (360 / (math.pi * 2)))
            if not self.rect.top - b < 0:
                self.pos = (self.pos[0], self.pos[1] + b)
        else:
            if self.rect.left <= 0:
                self.going_right = True
                self.angle = 90
                self.stored = pygame.transform.scale(pygame.image.load('Assets/plane.png.png').convert_alpha(),
                                                     (100, 32))
            self.pos = (self.pos[0] - 2, self.pos[1])
            a = dir_to(self.rect.center, pygame.mouse.get_pos())
            if 190 < a < 350:
                self.angle = a
            else:
                self.angle = 270
            b = 2 * math.cos(self.angle / (360 / (math.pi * 2)))
            if not self.rect.top - b < 0:
                self.pos = (self.pos[0], self.pos[1] + b)
        self.image = pygame.transform.rotate(self.stored, self.angle - 90)
        self.rect = self.image.get_rect(center=self.pos)


player_group = pygame.sprite.GroupSingle()
play = Player()
player_group.add(play)
