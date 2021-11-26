from abc import abstractmethod

import pygame

class Button(pygame.sprite.Sprite):

    @abstractmethod
    def __init__(self, screen, pathImage, x,y):
        super().__init__()
        self.screen=screen
        self.image=pygame.image.load(pathImage)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    @abstractmethod
    def pressed(self):
        pass
