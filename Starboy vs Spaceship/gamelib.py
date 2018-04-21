import pygame
from sys import exit
from pygame.locals import *
import random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 5 + 5 * random.random()

    def move(self):
        self.rect.top -= self.speed

    def boss_bullet_move(self):
        self.rect.top += self.speed
        direction = random.choice([-2, 2])
        self.rect.left += direction * self.speed

class Plane(pygame.sprite.Sprite):
    def __init__(self, plane_img, plane_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        for i in range(len(plane_rect)):
            self.image.append(plane_img.subsurface(plane_rect[i]).convert_alpha())
        self.rect = plane_rect[0]
        self.rect.topleft = init_pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs
       self.speed = 5 + 5 * random.random()
       self.down_index = 0

    def move_vertical(self):
        self.rect.top += self.speed

    def move_parallel(self):
        direction = random.choice([-1,1])
        self.rect.left += (direction * (self.speed))

class Friend(pygame.sprite.Sprite):
    def __init__(self, friend_img, friend_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = friend_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = friend_down_imgs
        self.speed = 2 + 5 * random.random()
        self.down_index = 0

    def move_vertical(self):
        self.rect.top += self.speed

    def move_parallel(self):
        direction = random.choice([-1,1])
        self.rect.left += (direction * (self.speed))

class Boss(pygame.sprite.Sprite):
    def __init__(self, boss_img, boss_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = boss_down_imgs
        self.speed = 1
        self.down_index = 0
        self.bullets = pygame.sprite.Group()
        self.is_hit = False
        self.show = False
        self.hp = 30

    def move_parallel(self):
        if self.rect.left <= 0:
            self.rect.left += self.speed
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left -= self.speed
        else:
            direction = random.choice([0, 1])
            self.rect.left += direction * self.speed

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def got_shot(self):
        self.hp -= 1
