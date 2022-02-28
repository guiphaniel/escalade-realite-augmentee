import math
import random

import pygame

from src.view.items.drawable import Drawable


class Target(Drawable):

    def __init__(self, parent):
        super().__init__(parent)
        self.size = (50, 50)
        self.rect = pygame.rect.Rect(random.randint(0, self.win.get_rect().width - self.size[0]), random.randint(0, self.win.get_rect().height - self.size[1]), 50, 50)
        self.sprite = pygame.transform.scale(pygame.image.load("view/images/sprites/target.png"), self.size)
        self.center = (self.rect.x + self.rect.width / 2.0, self.rect.y + self.rect.height / 2.0)
        self.radius = self.size[0] / 2
        self.ticks = pygame.time.get_ticks()

    def draw(self):
        self.win.blit(self.sprite, self.rect)

    def collide(self, point, radius):
        if (radius+self.radius) > math.sqrt((point[0]-self.rect.centerx)**2 + (point[1]-self.rect.centery)**2):
            self.sprite = pygame.transform.scale(pygame.image.load("view/images/sprites/success.png"), self.size)
            return True
        return False

    def failed(self):
        self.sprite = pygame.transform.scale(pygame.image.load("view/images/sprites/fail.png"), self.size)
