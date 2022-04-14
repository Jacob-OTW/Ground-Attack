import random
import pygame

import effects
import flare_obj
import projectiles
from projectiles import projectile_group
from effects import effect_group, Explosion
from player_obj import play
from settings import *


class Tank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(f'Assets/Vehicles/Tank/Norm.png').convert_alpha(), 0,
                                               0.4)
        a = random.uniform(0 + self.image.get_width() / 2, SCREEN_WIDTH - self.image.get_width() / 2)
        self.rect = self.image.get_rect(centerx=a)
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 100
        self.harm = []

    def update(self):
        if self.health > 0:
            for effect in effect_group.sprites():
                if type(effect) == effects.Explosion:
                    a = dis_to(self.rect.center, effect.rect.center)
                    if a <= 150:
                        self.health = 0
            for bullet in projectile_group.sprites():
                temp = self.mask.overlap(bullet.mask, (bullet.rect.x - self.rect.x, bullet.rect.y - self.rect.y))
                if temp:
                    match type(bullet):
                        case projectiles.Bomb:
                            Explosion.add_explosion((bullet.rect.centerx, self.rect.bottom))
                            bullet.kill()
                            self.health = 0
                        case projectiles.Bullet:
                            bullet.kill()
                            self.health -= 1
            if self.health <= 0:
                self.image = pygame.transform.rotozoom(pygame.image.load(f'Assets/Vehicles/Tank/Broken.png'), 0, 0.4)
        if self.rect.bottom <= SCREEN_HEIGHT:
            self.rect.y += 5


class Manpad(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.stored = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/Manpad/manpad.png').convert_alpha(), 0, 0.1)
        self.image = self.stored
        a = random.uniform(0 + self.image.get_width() / 2, SCREEN_WIDTH - self.image.get_width() / 2)
        self.rect = self.image.get_rect(centerx=a)
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 30
        self.harm = []
        self.fire_timer = random.randint(120, 300)
        self.timer = 0

    def update(self):
        # Fire
        self.timer += 1
        if self.timer >= self.fire_timer:
            enemy_projectile_group.add(Stinger(self.rect.center))
            self.fire_timer = random.randint(120, 300)
            self.timer = 0

        # Check if damage
        for effect in effect_group.sprites():
            if type(effect) == effects.Explosion:
                a = dis_to(self.rect.center, effect.rect.center)
                if a <= 150:
                    self.health = 0
        for bullet in projectile_group.sprites():
            temp = self.mask.overlap(bullet.mask, (bullet.rect.x - self.rect.x, bullet.rect.y - self.rect.y))
            if temp:
                match type(bullet):
                    case projectiles.Bomb:
                        Explosion.add_explosion((bullet.rect.centerx, self.rect.bottom))
                        bullet.kill()
                        self.health = 0
                    case projectiles.Bullet:
                        bullet.kill()
                        self.health -= 1
            if self.health <= 0:
                self.kill()

        # Drop asset
        if self.rect.bottom <= SCREEN_HEIGHT:
            self.rect.y += 5


class Stinger(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.stored = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/Manpad/stinger.png').convert_alpha(), 0, 0.1)
        self.image = self.stored
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        # Target
        self.target = play
        self.angle = dir_to(self.rect.center, self.target.rect.center)

        # Lifespan
        self.lifespan = 500

    def update(self):
        # Lifespan
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.kill()

        # Collision
        if self.mask.overlap(self.target.mask, (self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y)):
            Explosion.add_explosion(self.rect.center)
            if type(self.target) == flare_obj.Flare:
                self.target.kill()
            self.kill()

        # Delete
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # Track
        self.angle = dir_to(self.rect.center, self.target.rect.center)
        v = pygame.math.Vector2((7, 0)).rotate(self.angle)
        self.pos[0] += v[0]
        self.pos[1] -= v[1]

        # Update
        self.image = pygame.transform.rotate(self.stored, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)


vehicle_group = pygame.sprite.Group()
enemy_projectile_group = pygame.sprite.Group()
for j in range(1):
    vehicle_group.add(Manpad())
for i in range(0):
    vehicle_group.add(Tank())
