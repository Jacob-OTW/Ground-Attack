import pygame
import math
from settings import *
from effects import Smoke
from projectiles import projectile_group, Bullet
from pilot_obj import Pilot, pilot_group


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Image and mask
        self.stored = pygame.transform.scale(pygame.image.load('Assets/plane.png.png').convert_alpha(), (100, 32))
        self.image = self.stored
        self.rect = self.image.get_rect(left=0, top=SCREEN_HEIGHT / 8)
        self.mask = pygame.mask.from_surface(self.image)

        # Movement
        self.pos = pygame.math.Vector2((self.rect.x, self.rect.y))
        self.going_right = True
        self.angle = 0
        self.speed = 4
        self.m = 0.0
        self.v = 0

        # Health
        self.health = 100
        self.pilot = True

        # Weapons
        self.weapon = 'gun'
        self.max_gun = 150
        self.gun = self.max_gun
        self.bomb = True
        self.max_bomb = 120
        self.bomb_timer = 120

        # Countermeasure
        self.max_flares = 15
        self.flares = self.max_flares
        self.flare_timer = 0

    def update(self):
        if self.health > 0:
            self.move()
            self.keybinds()
            self.timers()
        else:
            if self.pilot:
                self.pilot = False
                pilot_group.add(Pilot(self.rect.center))
            self.angle = -80 if self.going_right else 260
            self.v = pygame.math.Vector2((4, 0)).rotate(self.angle)
            self.pos[0] += self.v[0]
            self.pos[1] -= self.v[1]

        self.image = pygame.transform.rotate(self.stored, self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)

    def local_pos(self, offset):  # Returns x and y in reference to rotated center of object, used for fixed ports
        v = pygame.math.Vector2(offset).rotate(self.angle)
        x = self.rect.centerx + v[0]
        y = self.rect.centery - v[1]
        return x, y

    def timers(self):
        # Flare timer
        if self.flare_timer >= 60:
            self.flares = min(self.flares + 1, 15)
            self.flare_timer = 0

        # Bomb Timer
        if not self.bomb:
            self.bomb_timer = min(self.bomb_timer + 1, self.max_bomb)
            if self.bomb_timer >= self.max_bomb:
                self.bomb = True

    def keybinds(self):
        # Shooting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.weapon == 'gun' and self.gun > 0:
                self.shoot()
                self.gun -= 1
        else:
            self.gun = min(self.gun + 0.5, self.max_gun)
        self.flare_timer += 1

    def shoot(self):
        p = self.local_pos((40, -2.5 if self.going_right else 2.5))
        projectile_group.add(Bullet(p, self.angle))
        Smoke.add_smoke(p, pygame.math.Vector2(-3, 0).rotate(self.angle))

    def move(self):
        # Turn
        if self.rect.right >= SCREEN_WIDTH if self.going_right else self.rect.left <= 0:
            self.going_right = not self.going_right
            self.angle += 180
            self.stored = pygame.transform.flip(
                pygame.transform.scale(pygame.image.load('Assets/plane.png.png').convert_alpha(), (100, 32)), False,
                False if self.going_right else True)

        # Move
        b = pygame.math.Vector2((2, 0)).rotate(self.angle)[1]
        self.v = 2 if self.going_right else -2, -b
        self.pos += self.v

        # Turn to mouse cursor
        d = dir_to(self.rect.center, pygame.mouse.get_pos())
        if d < 80 or d > 280 if self.going_right else 100 < d < 260:
            self.angle = d
        else:
            self.angle = 0 if self.going_right else 180


player_group = pygame.sprite.GroupSingle()
play = Player()
player_group.add(play)
