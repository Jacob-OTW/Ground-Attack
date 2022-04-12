import pygame
import math

from settings import *


def dir_to(mp, tp):
    x = tp[0] - mp[0]
    y = tp[1] - mp[1]
    if y == 0:
        return 90 if x > 0 else 270
    if y > 0:
        v = (math.atan(x / y)) * 57.29577951
    else:
        v = math.atan(x / y) * 57.29577951 + 180
    # v = round(v)
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
        self.going_right = True
        self.angle = 0
        self.speed = 4
        self.m = 0.0

    def update(self):
        if self.going_right:
            self.rect.x += self.speed
            self.rect.y -= math.sin(self.angle / Convert) * 2.5
            if self.rect.right >= SCREEN_WIDTH:
                self.going_right = False
            if pygame.mouse.get_pos()[0] > self.rect.x:
                self.angle = dir_to(self.rect, pygame.mouse.get_pos())
            else:
                self.angle = 0
            self.image = pygame.transform.rotate(self.stored, self.angle - 90)
        else:
            self.rect.x += self.speed * -1
            if self.rect.left <= 0:
                self.going_right = True
            if pygame.mouse.get_pos()[0] < self.rect.x:
                self.angle = dir_to(self.rect, pygame.mouse.get_pos())
            else:
                self.angle = 180
            self.image = pygame.transform.flip(self.stored, False, True)
            self.image = pygame.transform.rotate(self.image, self.angle - 90)


player_group = pygame.sprite.GroupSingle()
play = Player()
player_group.add(play)
