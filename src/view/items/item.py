from abc import abstractmethod

import pygame

import src
from src.view.items.item_display_type import itemDisplayType


class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.win = src.view.window.Window().win
        self.displayType = itemDisplayType.TOP_LEFT

    @abstractmethod
    def draw(self):
        pass

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y