import math
import random

import pygame.image

from src.view.items.item import Item


class Target(Item):

    def __init__(self):
        super().__init__()
        self.size = (50, 50)
        self.sprite = pygame.transform.scale(pygame.image.load("games/sprites/target.png"), self.size)
        self.rect = self.sprite.get_rect()
        self.rect.x = random.randint(0, self.win.get_rect().width - self.rect.width)
        self.rect.y = random.randint(0, self.win.get_rect().height - self.rect.height)
        self.center = [self.rect.x + self.rect.width / 2.0, self.rect.y + self.rect.height / 2.0]
        self.radius = self.rect.height / 2.0
        self.ticks = pygame.time.get_ticks()

    def draw(self):
        self.win.blit(self.sprite, self.rect)

    def collide(self, polygon):
        if polygon.colliderect(self.rect):
            self.sprite = pygame.transform.scale(pygame.image.load("games/sprites/success.png"), self.size)
            return True
        return False

    def failed(self):
        self.sprite = pygame.transform.scale(pygame.image.load("games/sprites/fail.png"), self.size)
