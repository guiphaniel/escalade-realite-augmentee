from abc import abstractmethod

import pygame
import src
from src.utils.events.motion_listener import MotionListener
from src.utils.events.mouse_listener import MouseListener
from src.view.items.item import Item


class AbstractInternalFrame(Item, MouseListener, MotionListener):
    def __init__(self, parent, rect, bgColor = (50, 50, 50), bgImage = None):
        Item.__init__(self)
        MouseListener.__init__(self)
        MotionListener.__init__(self)

        self.parent = parent
        self.held = False

        self.snappingRect = rect.copy()
        self.snappingRect.h = 10

        rect.y = rect.y + self.snappingRect.h #let some space for the bar
        self.rect = rect

        self.bgColor = bgColor
        if bgImage:
            self.bgImage = pygame.transform.scale(pygame.image.load(bgImage), (self.rect.w, self.rect.h))
        else:
            self.bgImage = None
        self.win = src.view.window.Window().win
        self.items = []

    @abstractmethod
    def execute(self):
        pass

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
        elif e.type == pygame.MOUSEBUTTONUP:
            if self.held:
                self.held = False
                return True

        return False

    def onMotionEvent(self, e) -> bool:
        if self.held:
            x, y = pygame.mouse.get_pos()
            self.snappingRect = self.snappingRect.move(x - self.lastMousePosX, y - self.lastMousePosY)
            self.rect = self.rect.move(x - self.lastMousePosX, y - self.lastMousePosY)
            self.lastMousePosX, self.lastMousePosY = x, y
            self.parent.repaintAll()
            return True

        return False