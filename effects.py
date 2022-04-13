import pygame
import random
from settings import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.stored = pygame.image.load('Assets/explosion.png').convert_alpha()
        self.size = 0.1
        self.pos = pos
        self.image = pygame.transform.rotozoom(self.stored, 0, self.size)
        self.rect = self.image.get_rect(center=pos)
        self.opacity = 255

    def update(self):
        self.image = pygame.transform.rotozoom(self.stored, 0, self.size)
        self.rect = self.image.get_rect(center=self.pos)
        if self.size <= 1:
            self.size += 0.1
        else:
            self.opacity -= 4.5
            self.image.set_alpha(self.opacity)
            if self.opacity <= 0:
                self.kill()


class Smoke(pygame.sprite.Sprite):
    @classmethod
    def add_smoke(cls, pos, m_vec=None):
        effect_group.add(Smoke(pos, m_vec))

    def __init__(self, pos, m_vec=None):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Assets/smoke.png').convert_alpha(), (20, 20))
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.opacity = 255
        self.fall_speed = 0.3
        self.vec = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.m_vec = m_vec

    def update(self):
        self.pos = (self.pos[0], self.pos[1] + self.fall_speed)
        self.pos += self.vec
        if self.m_vec:
            self.pos += pygame.math.Vector2(self.m_vec)
        self.rect.center = self.pos
        self.image.set_alpha(self.opacity)
        self.opacity -= 5
        if self.opacity <= 0:
            self.kill()


effect_group = pygame.sprite.Group()
