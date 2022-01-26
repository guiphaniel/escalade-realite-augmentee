import pygame

from src.view.utils.events.mouse_listener import MouseListener
from src.view.utils.items.item import Item


class Button(Item, MouseListener):
    def __init__(self, x, y, w, h, text=None):
        Item.__init__(self)
        MouseListener.__init__(self)

        # init textures
        self.bgColor = (255, 255, 255)
        self.borderColor = (0, 0, 0)
        self.padding = 10
        self.borderWidth = 10
        self.borderRadius = 10
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.setText(text)

        # init events
        self.actionListeners = []

    def setText(self, text, textColor=(0, 0, 0), textSize=40, textFont="view/fonts/All the Way to the Sun.otf"):
        self.__textSurface = None
        if not text:
            return
        font = pygame.font.SysFont(textFont, textSize)
        self.__textSurface = font.render(text, True, textColor)
        rect = self.__textSurface.get_rect()
        self.w = rect.w
        self.h = rect.h

    def setStyle(self, bgColor, borderColor, padding, borderWidth, borderRadius):
        self.bgColor = bgColor
        self.borderColor = borderColor
        self.padding = padding
        self.borderWidth = borderWidth
        self.borderRadius = borderRadius

    def draw(self):
        pygame.draw.rect(self.win, self.borderColor, pygame.rect.Rect(self.x - self.borderWidth, self.y - self.borderWidth, self.w + self.borderWidth * 2 + self.padding * 2, self.h + self.borderWidth * 2 + self.padding * 2), 0, self.borderRadius)  # border
        pygame.draw.rect(self.win, self.bgColor, pygame.rect.Rect(self.x, self.y, self.w + self.padding * 2, self.h + self.padding * 2), 0, self.borderRadius)  # inner
        if self.__textSurface:
            self.win.blit(self.__textSurface, pygame.rect.Rect(self.x + self.padding, self.y+self.padding, self.w, self.h))

    def update(self):
        pygame.display.update(
            pygame.rect.Rect(self.x - self.borderRadius, self.y - self.borderRadius,
                             self.w + self.padding * 2 + self.borderRadius * 2,
                             self.h + self.padding * 2 + self.borderRadius * 2))

    def addActionListener(self, l):
        self.actionListeners.append(l)

    def removeActionListener(self, l):
        self.actionListeners.remove(l)

    def onMouseEvent(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if pygame.rect.Rect(self.x - self.borderRadius, self.y - self.borderRadius, self.w + self.padding * 2 + self.borderRadius * 2, self.h + self.padding * 2 + self.borderRadius * 2).collidepoint(x, y):
                self.notifyAllActionListeners()

    def notifyAllActionListeners(self):
        for l in self.actionListeners:
            l.actionPerformed(self)
