from abc import abstractmethod

import pygame
import src


class AbstractFrame:
    def __init__(self, bgColor=(0, 0, 0), bgImage=None):
        self.rect = pygame.rect.Rect(0, 0, 1920, 1080)
        self.padding = 0

        self.bgColor = bgColor
        if bgImage:
            self.bgImage = pygame.image.load(bgImage)
        else:
            self.bgImage = None
        self.win = src.view.window.Window().win
        self.items = []

    def add(self, item):
        item.parent = self
        self.items.append(item)

    def remove(self, item):
        item.parent = None
        self.items.remove(item)

    def removeAll(self):
        for i in self.items:
            i.parent = None
        self.items.clear()

    def repaint(self, item):
        skip = True
        for i in self.items:
            if i == item:
                skip = False
            if not skip:
                i.draw()
        pygame.display.flip()

    def repaintAll(self):
        if self.bgImage:
            self.win.blit(self.bgImage, (0, 0))
        else:
            self.win.fill(self.bgColor)
        for i in self.items:
            i.draw()
        pygame.display.flip()
