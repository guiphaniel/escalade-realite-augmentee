from abc import abstractmethod

import pygame
from pygame.sprite import Sprite

import src
from src.view.items.item_display_type import itemDisplayType


class Drawable(Sprite):
    def __init__(self, parent, x, y, w, h):
        Sprite.__init__(self)
        self.parent = parent
        self.win = src.view.window.Window().win
        self.displayType = itemDisplayType.TOP_LEFT
        self.rect = pygame.rect.Rect(0,0,0,0)

    @abstractmethod
    def draw(self):
        pass

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y