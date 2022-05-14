import pygame
from settings import *


class Pilot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pilot_image = pygame.transform.scale(pygame.image.load('Assets/Pilot.png').convert_alpha(), (100, 100))
        self.image = self.pilot_image
        self.rect = self.image.get_rect(center=pos)
        self.angle = 0
        self.swing_right = True
        self.swing_speed = 1

    def update(self):
        if self.swing_right:
            self.angle += self.swing_speed
            if self.angle >= 45:
                self.swing_right = False
        else:
            self.angle -= self.swing_speed
            if self.angle <= -45:
                self.swing_right = True
        self.image = pygame.transform.rotate(self.pilot_image, self.angle)
        self.rect.centery += 1
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


pilot_group = pygame.sprite.Group()
