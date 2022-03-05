import pygame

from src.view.items.drawable import Drawable
from src.view.items.list_item import ListItem

class List(Drawable):

    def __init__(self, parent, x, y):
        Drawable.__init__(self, parent)
        self._selectedItem = None
        self.items = []
        self.bgColor = (200, 200, 200)
        self.padding = 5
        self.rect = pygame.rect.Rect(x, y, 0, 0)

        self.listListeners = []

    def draw(self):
        if len(self.items) <= 0:
            return

        self.shrinkToFit()
        pygame.draw.rect(self.win, self.bgColor, self.rect)

        firstItem = self.items[0]
        firstItem.rect.y = self.rect.y + self.padding
        firstItem.draw()

        for index, item in enumerate(self.items[1:]):
            prevItem = self.items[index] # only use index and not index - 1, as enumerate already makes it start at 0
            item.rect.y = prevItem.rect.y + prevItem.rect.h + self.padding
            item.draw()

    @property
    def selectedItem(self):
        return self._selectedItem

    @selectedItem.setter
    def selectedItem(self, item):
        if item:
            item.bgColor = ListItem.secondaryColor
            if self._selectedItem:
                self._selectedItem.bgColor = ListItem.primaryColor


        self._selectedItem = item
        self.notifyAllListListeners()

    def shrinkToFit(self):
        maxX = 0
        maxY = 0
        for i in self.items:
            iX = i.rect.x - self.rect.x + i.rect.w
            if iX > maxX:
                maxX = iX

            iY = i.rect.y - self.rect.y + i.rect.h
            if iY > maxY:
                maxY = iY

        self.rect.w = maxX + self.padding
        self.rect.h = maxY + self.padding

    def addListListener(self, l):
        self.listListeners.append(l)

    def removeListListener(self, l):
        self.listListeners.remove(l)

    def notifyAllListListeners(self):
        for l in self.listListeners:
            l.valueChanged(self)