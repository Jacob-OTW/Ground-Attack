import random
import effects
import flare_obj
import player_obj
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


class ManPad(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.stored = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/ManPad/ManPad.png').convert_alpha(),
                                                0, 0.1)
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
        self.stored = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/ManPad/stinger.png').convert_alpha(),
                                                0, 0.1)
        self.image = self.stored
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        # Target
        self.target = play
        self.angle = dir_to(self.rect.center, self.target.rect.center)
        self.speed = 5.5

        # Lifespan
        self.lifespan = 500

    def predicted_los(self, r=0):
        if self.target and self.target.alive():
            t = dis_to(self.rect.center, self.predicted_los(r=r + 1) if r <= 2 else self.target.rect.center) / 6
            return self.target.rect.centerx + (self.target.v[0] * int(t)), self.target.rect.centery + (
                    self.target.v[1] * int(t))
        return self.target.rect.center

    def update(self):
        # Lifespan
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.kill()

        # Collision
        if self.mask.overlap(self.target.mask, (self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y)):
            Explosion.add_explosion(self.rect.center, e_type='Air')
            match type(self.target):
                case flare_obj.Flare:
                    self.target.kill()
                case player_obj.Player:
                    self.target.health -= 15
            self.kill()

        # Delete
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # Track
        self.angle = dir_to(self.rect.center, self.predicted_los())
        v = pygame.math.Vector2((self.speed, 0)).rotate(self.angle)
        self.pos[0] += v[0]
        self.pos[1] -= v[1]

        # Update
        self.image = pygame.transform.rotate(self.stored, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)


class AAA(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 0.5

        self.image = pygame.Surface((200 * self.size, 170 * self.size), pygame.SRCALPHA, 32)
        a = random.uniform(0 + self.image.get_width() / 2, SCREEN_WIDTH - self.image.get_width() / 2)
        self.rect = self.image.get_rect(centerx=a)

        # Images
        self.body = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/AAA/body.png').convert_alpha(), 0,
                                              self.size)
        self.body_rect = self.body.get_rect(midbottom=(100 * self.size, 170 * self.size))
        self.turret = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/AAA/turret.png').convert_alpha(), 0,
                                                self.size)
        self.turret_rect = self.turret.get_rect(midbottom=(100 * self.size, 170 * self.size))
        self.barrel = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/AAA/barrel.png').convert_alpha(), 0,
                                                self.size)
        self.barrel_rect = self.barrel.get_rect(center=(100 * self.size, 105 * self.size))

        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.health = 100
        self.harm = []
        self.target = play

        self.bullets = 15
        self.timer = 0

    def predicted_los(self, r=0):
        if self.target and self.target.alive():
            t = dis_to(self.rect.center, self.predicted_los(r=r + 1) if r <= 2 else self.target.rect.center) / 6
            return self.target.rect.centerx + (self.target.v[0] * int(t)), self.target.rect.centery + (
                    self.target.v[1] * int(t))
        return self.target.rect.center

    def load_images(self):
        self.image = pygame.Surface((200 * self.size, 170 * self.size), pygame.SRCALPHA, 32)
        self.angle = dir_to(self.rect.center, self.predicted_los())
        self.barrel = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/AAA/barrel.png').convert_alpha(),
                                                self.angle, self.size)
        self.barrel_rect = self.barrel.get_rect(center=(80 * self.size, 105 * self.size))
        self.image.blit(self.body, self.body_rect)
        self.image.blit(self.turret, self.turret_rect)
        self.image.blit(self.barrel, self.barrel_rect)

    def update(self):
        if self.health > 0:
            self.load_images()
            self.mask = pygame.mask.from_surface(self.image)

            # Shoot
            self.timer += 1
            if self.timer >= 240:
                if self.bullets > 0:
                    enemy_projectile_group.add(EnemyBullet(self.rect.center, self.angle))
                    self.bullets -= 1
                else:
                    self.bullets = 15
                    self.timer = 0

            # Explosion damage
            for effect in effect_group.sprites():
                if type(effect) == effects.Explosion:
                    a = dis_to(self.rect.center, effect.rect.center)
                    if a <= 150:
                        self.health = 0

            # Bullet damage
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

            # Die
            if self.health <= 0:
                self.image = pygame.transform.rotozoom(pygame.image.load(f'Assets/Vehicles/AAA/broken.png'), 0,
                                                       self.size)
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        # Fall
        if self.rect.bottom <= SCREEN_HEIGHT:
            self.rect.y += 5


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/bullet.png').convert_alpha(), angle, 0.4)
        self.rect = self.image.get_rect(center=self.pos)
        angle += random.uniform(-1.5, 1.5)
        self.mask = pygame.mask.from_surface(self.image)
        self.vec = pygame.math.Vector2((6, 0)).rotate(angle)

    def update(self):
        # Delete
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # Move
        self.pos[0] += self.vec[0]
        self.pos[1] -= self.vec[1]

        # Update
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        # Collide
        if self.mask.overlap(play.mask, (play.rect.x - self.rect.x, play.rect.y - self.rect.y)):
            Explosion.add_explosion(self.rect.center, e_type='Air', size=0.1)
            play.health -= 1
            self.kill()


vehicle_group = pygame.sprite.Group()
enemy_projectile_group = pygame.sprite.Group()
for h in range(1):
    vehicle_group.add(AAA())
for j in range(1):
    vehicle_group.add(ManPad())
for i in range(1):
    vehicle_group.add(Tank())
