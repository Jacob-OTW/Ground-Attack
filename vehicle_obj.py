import random
import pygame
from bullet_obj import bullet_group
from settings import *


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, veh_type):
        super().__init__()
        self.veh_type = veh_type
        self.image = pygame.transform.rotozoom(pygame.image.load(f'Assets/Vehicles/{veh_type}/Norm.png').convert_alpha(), 0, 0.4)
        a = random.uniform(0 + self.image.get_width()/2, SCREEN_WIDTH-self.image.get_width()/2)
        self.rect = self.image.get_rect(centerx=a)
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 30

    def update(self):
        if self.health > 0:
            for bullet in bullet_group.sprites():
                temp = self.mask.overlap(bullet.mask, (bullet.rect.x - self.rect.x, bullet.rect.y - self.rect.y))
                if temp:
                    bullet.kill()
                    self.health -= 1
                    if self.health <= 0:
                        self.image = pygame.transform.rotozoom(pygame.image.load(f'Assets/Vehicles/{self.veh_type}/Broken.png'), 0, 0.4)
        if self.rect.bottom <= SCREEN_HEIGHT:
            self.rect.y += 5


vehicle_group = pygame.sprite.Group()
for i in range(10):
    vehicle_group.add(Vehicle('Tank'))
