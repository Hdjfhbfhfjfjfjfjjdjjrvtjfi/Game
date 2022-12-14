import pygame
import random
from pygame.math import Vector2


class Player(pygame.sprite.Sprite):
    WALK_SPEED = 3
    RUN_SPEED = 6

    def __init__(self, group, cls):
        super().__init__()
        self.weapon = 0
        self.health = 100
        self.weapon_magazine = [10, 30, 5]
        self.weapon_damage = (10, 15, 10)
        self.shoot_cooldown = [0, 0, 0]
        self.position = Vector2(200, 200)
        self.image = pygame.Surface((20, 20))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.bullet_class = cls
        self.direction = pygame.math.Vector2(0, 0)
        self.add(group)

    def update(self, group, mouse_x, mouse_y):
        keys = pygame.key.get_pressed()
        self.switch_weapon(keys)
        if keys[pygame.K_LSHIFT]:
            self.movement(keys, self.RUN_SPEED)
        elif not keys[pygame.K_LSHIFT]:
            self.movement(keys, self.WALK_SPEED)
        self.rect.center = self.position
        if pygame.mouse.get_pressed()[0] and self.shoot_cooldown[self.weapon] == 0:
            self.strike(group, mouse_x, mouse_y)
        self.shoot_cooldown[self.weapon] = 0 if self.shoot_cooldown[self.weapon] == 0 else self.shoot_cooldown[self.weapon] - 1

    def switch_weapon(self, keys):
        if keys[pygame.K_1]:
            self.weapon = 0
        elif keys[pygame.K_2]:
            self.weapon = 1
        elif keys[pygame.K_3]:
            self.weapon = 2

    def movement(self, keys, move_mode):
        self.direction = Vector2(0, 0)
        if keys[pygame.K_w]:
            self.direction = self.direction + Vector2(0, -move_mode)
        if keys[pygame.K_s]:
            self.direction = self.direction + Vector2(0, move_mode)
        if keys[pygame.K_a]:
            self.direction = self.direction + Vector2(-move_mode, 0)
        if keys[pygame.K_d]:
            self.direction = self.direction + Vector2(move_mode, 0)
        self.position += self.direction
        if self.position[0] > 1670:
            self.position[0] = 1670
        elif self.position[0] < 10:
            self.position[0] = 10
        if self.position[1] > 1040:
            self.position[1] = 1040
        elif self.position[1] < 10:
            self.position[1] = 10

    def strike(self, group, mouse_x, mouse_y):
        match self.weapon:
            case 0:
                self.pistol(group, mouse_x, mouse_y, self.weapon)
            case 1:
                self.automatic_rifle(group, mouse_x, mouse_y, self.weapon)
            case 2:
                self.shotgun(group, mouse_x, mouse_y, self.weapon)

    def pistol(self, group, mouse_x, mouse_y, weapon):
        if self.weapon_magazine[self.weapon]:
            self.bullet_class(self.rect.centerx, self.rect.centery, mouse_x, mouse_y, group, self.weapon_damage[weapon])
            self.shoot_cooldown[self.weapon] = 30
            self.weapon_magazine[self.weapon] -= 1
        else:
            self.weapon_magazine[self.weapon] = 10
            self.shoot_cooldown[self.weapon] = 180

    def automatic_rifle(self, group, mouse_x, mouse_y, weapon):
        if self.weapon_magazine[self.weapon]:
            self.bullet_class(self.rect.centerx, self.rect.centery, mouse_x, mouse_y, group, self.weapon_damage[weapon])
            self.shoot_cooldown[self.weapon] = 10
            self.weapon_magazine[self.weapon] -= 1
        else:
            self.weapon_magazine[self.weapon] = 30
            self.shoot_cooldown[self.weapon] = 180

    def shotgun(self, group, mouse_x, mouse_y, weapon):
        if self.weapon_magazine[self.weapon] != 0:
            direction = pygame.math.Vector2(mouse_x - self.rect.centerx, mouse_y - self.rect.centery).normalize()
            for _ in range(10):
                self.bullet_class(self.rect.centerx, self.rect.centery,
                                  direction.rotate(random.randint(-12, 12))[0] + self.rect.centerx,
                                  direction.rotate(random.randint(-12, 12))[1] + self.rect.centery, group,
                                  self.weapon_damage[weapon])
            self.shoot_cooldown[self.weapon] = 60
            self.weapon_magazine[self.weapon] -= 1
        else:
            print(1)
            self.weapon_magazine[self.weapon] = 5
            self.shoot_cooldown[self.weapon] = 300

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.kill()


