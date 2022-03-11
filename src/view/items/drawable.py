from abc import abstractmethod

import pygame
from pygame.sprite import Sprite

import src
from src.view.items.item_display_type import ItemDisplayType


class Drawable(Sprite):
    def __init__(self, displayType=ItemDisplayType.TOP_LEFT):
        Sprite.__init__(self)
        self._parent = None
        self.win = src.view.window.Window().win
        self.displayType = displayType

    @abstractmethod
    def draw(self):
        pass

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, newParent):
        self._parent = newParent

