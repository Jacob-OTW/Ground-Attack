import random

import pygame

import player_obj
import vehicle_obj
from settings import *
from effects import Smoke
from vehicle_obj import enemy_projectile_group


class Flare(pygame.sprite.Sprite):
    def __init__(self, pos, r, play):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/flares.png').convert_alpha(), 0, 0.5)
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.v = pygame.math.Vector2((-2.5 if r else 2.5, -5))

        # Timers
        self.timer = 0

        # Draw stinger away from Target
        for projectile in enemy_projectile_group.sprites():
            if type(projectile) == vehicle_obj.Stinger:
                if type(projectile.target) == player_obj.Player and random.randint(0, 1) == 1:
                    projectile.target = self

    def update(self):
        # Update pos
        self.pos += self.v
        self.v[0] *= 0.95
        if self.v[1] < 4:
            self.v[1] += 1
        self.rect.center = self.pos

        # Timers
        self.timer += 1
        if self.timer % 3 == 0:
            Smoke.add_smoke(self.pos)

        # Destroy self
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


flare_group = pygame.sprite.Group()
