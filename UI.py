import pygame
from settings import *
from player_obj import play as player


class weapon_UI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {'gun': pygame.image.load('Assets/UI/UI_gun.png').convert_alpha(),
                       'bomb': pygame.image.load('Assets/UI/UI_missile.png').convert_alpha()}
        self.img_surface = pygame.transform.scale(self.images[player.weapon], (300, 150))
        self.missile_load = pygame.Surface((150, 150))
        self.missile_load.fill('Green')
        self.image = pygame.Surface((300, 150))
        self.rect = self.image.get_rect(left=0, top=0)

    def update(self):
        self.img_surface = pygame.transform.scale(self.images[player.weapon], (300, 150))
        # Missile rect
        loading_rect = pygame.transform.scale(self.missile_load, (150, (player.bomb_timer / 0.8)))
        loading_rect.set_alpha(153)

        # Gun rect
        gun_loading_rect = pygame.transform.scale(self.missile_load, (150, player.gun))
        gun_loading_rect.set_alpha(153)

        # draw
        self.image.blit(self.img_surface, (0, 0))
        self.image.blit(loading_rect, (150, 150 - (player.bomb_timer / (player.max_bomb / 150))))
        self.image.blit(gun_loading_rect, (0, 150 - player.gun))


class flare_ui(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_surface = pygame.image.load('Assets/UI/flares.png').convert_alpha()
        self.load = pygame.Surface((150, 150))
        self.load.fill('Green')
        self.image = pygame.Surface((150, 150))
        self.rect = self.image.get_rect(left=300, top=0)

    def update(self):
        # flare rect
        loading = pygame.transform.scale(self.load, (150, player.flares / (player.max_flares / 150)))
        loading_rect = loading.get_rect(midbottom=(75, 150))
        loading.set_alpha(153)

        # draw
        self.image.blit(self.img_surface, (0, 0))
        self.image.blit(loading, loading_rect)


ui_group = pygame.sprite.Group()
ui_group.add(weapon_UI())
ui_group.add(flare_ui())
