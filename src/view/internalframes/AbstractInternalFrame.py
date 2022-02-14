from abc import abstractmethod

import pygame
import src
from src.utils.events.motion_listener import MotionListener
from src.utils.events.mouse_listener import MouseListener
from src.view.items.item import Item


class AbstractInternalFrame(Item, MouseListener, MotionListener):
    def __init__(self, parent, coordinates, bgColor = (50, 50, 50), bgImage = None):
        Item.__init__(self)
        MouseListener.__init__(self)
        MotionListener.__init__(self)

        self.parent = parent
        self.held = False

        self.snappingRect = pygame.rect.Rect(coordinates[0], coordinates[1], 0, 10)

        self.rect = self.snappingRect.copy()
        self.rect.y += self.snappingRect.h  # let some space for the bar

        self.padding = 10

        self.bgColor = bgColor
        if bgImage:
            self.bgImage = pygame.transform.scale(pygame.image.load(bgImage), (self.rect.w, self.rect.h))
        else:
            self.bgImage = None
        self.win = src.view.window.Window().win
        self.items = []

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items.remove(item)

    def removeAll(self):
        self.items.clear()

    def repaint(self, item):
        skip = True
        for i in self.items:
            if i == item:
                skip = False
            if not skip:
                i.draw()
        self.parent.repaint(self)

    def repaintAll(self):
        pygame.draw.rect(self.win, (127,127,127), self.snappingRect)
        if self.bgImage:
            self.win.blit(self.bgImage, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(self.win, self.bgColor, self.rect)
        for i in self.items:
            i.draw()
        self.parent.repaint(self)

    def draw(self):
        pygame.draw.rect(self.win, (127, 127, 127), self.snappingRect)
        if self.bgImage:
            self.win.blit(self.bgImage, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(self.win, self.bgColor, self.rect)
        for i in self.items:
            i.draw()

    def onMouseEvent(self, e) -> bool:
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.snappingRect.collidepoint(pygame.mouse.get_pos()):
                self.lastMousePosX, self.lastMousePosY = pygame.mouse.get_pos()
                self.held = True
                return True
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True  # returns True as we want it to block underneath items to be triggered by the event manager
        elif e.type == pygame.MOUSEBUTTONUP:
            if self.held:
                needsToBeRepainted = False
                # make sure the frame doesn't exceed parent's borders
                if self.rect.x < self.parent.rect.x:
                    self.move(self.parent.rect.x - self.rect.x, 0)
                    needsToBeRepainted = True
                if self.rect.x + self.rect.w > self.parent.rect.w:
                    self.move(self.parent.rect.w - (self.rect.x + self.rect.w), 0)
                    needsToBeRepainted = True
                if self.snappingRect.y < self.parent.rect.y:
                    self.move(0, self.parent.rect.y - self.snappingRect.y)
                    needsToBeRepainted = True
                if self.rect.y + self.rect.h > self.parent.rect.h:
                    self.move(0, self.parent.rect.h - (self.rect.y + self.rect.h))
                    needsToBeRepainted = True

                if needsToBeRepainted:
                    self.parent.repaintAll()

                self.held = False
                return True

        return False

    def onMotionEvent(self, e) -> bool:
        if self.held:
            x, y = pygame.mouse.get_pos()
            newX, newY = x - self.lastMousePosX, y - self.lastMousePosY
            self.lastMousePosX, self.lastMousePosY = x, y

            self.move(newX, newY)

            self.parent.repaintAll()
            return True

        return False

    def move(self, x, y):
        self.snappingRect = self.snappingRect.move(x, y)
        self.rect = self.rect.move(x, y)
        for i in self.items:
            i.move(x, y)

    def shrinkToFit(self):
        maxX = 0
        maxY = 0
        for i in self.items:
            iX = i.rect.x - self.rect.x + i.rect.w
            if iX > maxX:
                maxX = iX

            iY = i.rect.y - self.rect.y + i.rect.w
            if iY > maxY:
                maxY = iY
        
        self.rect.w = maxX + self.padding
        self.rect.h = maxY + self.padding
        self.snappingRect.w = self.rect.w