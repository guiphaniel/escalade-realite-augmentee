import math
import random

import pygame.image

from src.view.items.item import Item


class Target(Item):

    def __init__(self, parent):
        super().__init__(parent, 0, 0, 50, 50)
        self.size = (self.rect.w, self.rect.h)
        self.sprite = pygame.transform.scale(pygame.image.load("view/images/sprites/target.png"), self.size)
        self.rect.x = random.randint(0, self.win.get_rect().width - self.rect.width)
        self.rect.y = random.randint(0, self.win.get_rect().height - self.rect.height)
        self.center = [self.rect.x + self.rect.width / 2.0, self.rect.y + self.rect.height / 2.0]
        self.radius = self.rect.height / 2.0
        self.ticks = pygame.time.get_ticks()

    def draw(self):
        self.win.blit(self.sprite, self.rect)

    def collide(self, polygon):
        if polygon.colliderect(self.rect):
            self.sprite = pygame.transform.scale(pygame.image.load("view/images/sprites/success.png"), self.size)
            return True
        return False

    def failed(self):
        self.sprite = pygame.transform.scale(pygame.image.load("view/images/sprites/fail.png"), self.size)
