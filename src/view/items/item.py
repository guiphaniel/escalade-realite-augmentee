from abc import abstractmethod

import pygame
from pygame.sprite import Sprite

import src
from src.view.items.item_display_type import itemDisplayType


class Item(Sprite):
    def __init__(self, parent, x, y, w, h):
        Sprite.__init__(self)
        self.parent = parent
        self.rect = pygame.rect.Rect(x + parent.rect.x + parent.padding, y + parent.rect.y + parent.padding, w, h)
        self.win = src.view.window.Window().win
        self.displayType = itemDisplayType.TOP_LEFT

    @abstractmethod
    def draw(self):
        pass

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y