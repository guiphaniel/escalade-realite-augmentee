from abc import abstractmethod

import pygame

import src


class Item(pygame.sprite.Sprite):
    def __init__(self):
        self.win = src.view.window.Window().win