import pygame
import math
from settings import *
from effects import Smoke
from projectiles import projectile_group, Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.stored = pygame.transform.scale(pygame.image.load('Assets/plane.png.png').convert_alpha(), (100, 32))
        self.image = self.stored
        self.rect = self.image.get_rect(left=0, top=SCREEN_HEIGHT / 8)
        self.pos = pygame.math.Vector2((self.rect.x, self.rect.y))
        self.going_right = True
        self.angle = 0
        self.speed = 4
        self.m = 0.0

    def update(self):
        self.move()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        v = pygame.math.Vector2((40, -2.5 if self.going_right else 2.5)).rotate(self.angle)
        x = self.rect.centerx + v[0]
        y = self.rect.centery - v[1]
        p = (x, y)
        projectile_group.add(Bullet(p, self.angle))
        Smoke.add_smoke(p, pygame.math.Vector2(-3, 0).rotate(self.angle))

    def move(self):
        if self.going_right:
            if self.rect.right >= SCREEN_WIDTH:
                self.going_right = False
                self.angle = 180
                self.stored = pygame.transform.flip(
                    pygame.transform.scale(pygame.image.load('Assets/plane.png.png').convert_alpha(), (100, 32)), False,
                    True)
            self.pos += pygame.math.Vector2((2, 0))
            d = dir_to(self.rect.center, pygame.mouse.get_pos())
            if d < 80 or d > 280:
                self.angle = d
            else:
                self.angle = 0
            b = -2 * math.sin(math.radians(self.angle))
            if not self.rect.top - b < 0:
                self.pos[1] += b
        else:
            if self.rect.left <= 0:
                self.going_right = True
                self.angle = 0
                self.stored = pygame.transform.scale(pygame.image.load('Assets/plane.png.png').convert_alpha(),
                                                     (100, 32))
            self.pos -= pygame.math.Vector2((2, 0))
            a = dir_to(self.rect.center, pygame.mouse.get_pos())
            if 100 < a < 260:
                self.angle = a
            else:
                self.angle = 180
            b = -2 * math.sin(math.radians(self.angle))
            if not self.rect.top - b < 0:
                self.pos[1] += b
        self.image = pygame.transform.rotate(self.stored, self.angle)
        self.rect = self.image.get_rect(center=self.pos)


player_group = pygame.sprite.GroupSingle()
play = Player()
player_group.add(play)
