import pygame

from src.view.events.mouse_listener import MouseListener
from src.view.items.item import Item


# TODO: rajouter la gestion d'une bgImage
class Button(Item, MouseListener):
    def __init__(self, x, y, w=40, h=20, text=None):
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

        self.__updateRect()
        self.setText(text)

        # init events
        self.active = True
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
        self.__updateRect()

    def setStyle(self, bgColor, borderColor, padding, borderWidth, borderRadius):
        self.bgColor = bgColor
        self.borderColor = borderColor
        self.padding = padding
        self.borderWidth = borderWidth
        self.borderRadius = borderRadius
        self.__updateRect()

    def draw(self):
        pygame.draw.rect(self.win, self.borderColor, self.rect, 0, self.borderRadius)  # border
        pygame.draw.rect(self.win, self.bgColor,
                         pygame.rect.Rect(self.x, self.y, self.w + self.padding * 2, self.h + self.padding * 2), 0,
                         self.borderRadius)  # inner
        if self.__textSurface:
            self.win.blit(self.__textSurface,
                          pygame.rect.Rect(self.x + self.padding, self.y + self.padding, self.w, self.h))

        if not self.active:
            s = pygame.Surface((self.rect.w - self.borderWidth*2, self.rect.h - self.borderWidth*2))  # the size of your rect
            s.set_alpha(128)  # alpha level
            s.fill((0, 0, 0))  # this fills the entire surface
            self.win.blit(s, (self.rect.x + self.borderWidth, self.rect.y + self.borderWidth))

    def update(self):
        pygame.display.update(self.rect)

    def addActionListener(self, l):
        self.actionListeners.append(l)

    def removeActionListener(self, l):
        self.actionListeners.remove(l)

    def onMouseEvent(self, e):
        if not self.active:
            return

        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if pygame.rect.Rect(self.x - self.borderRadius, self.y - self.borderRadius,
                                self.w + self.padding * 2 + self.borderRadius * 2,
                                self.h + self.padding * 2 + self.borderRadius * 2).collidepoint(x, y):
                self.notifyAllActionListeners()

    def notifyAllActionListeners(self):
        for l in self.actionListeners:
            l.actionPerformed(self)

    # updates the outer rect (hitbox)
    def __updateRect(self):
        self.rect = pygame.rect.Rect(self.x - self.borderWidth, self.y - self.borderWidth,
                                     self.w + self.padding * 2 + self.borderWidth * 2,
                                     self.h + self.padding * 2 + self.borderWidth * 2)
