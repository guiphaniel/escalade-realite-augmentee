import pygame

from src.utils.events.mouse_listener import MouseListener
from src.view.items.drawable import Drawable


# TODO: rajouter la gestion d'une bgImage
class Button(Drawable, MouseListener):
    def __init__(self, x, y, w=40, h=20, text=None):
        Drawable.__init__(self)
        MouseListener.__init__(self)

        # init textures
        self.bgColor = (255, 255, 255)
        self.borderColor = (0, 0, 0)
        self.padding = 10
        self.borderWidth = 10
        self.borderRadius = 10

        # self.rect is equivalent to the outer rect of the button (margin + borders included)
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(0, 0, w, h)
        self.rect.w += self.padding * 2 + self.borderWidth * 2
        self.rect.h += self.padding * 2 + self.borderWidth * 2

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
        self.rect.w = rect.w + self.padding * 2 + self.borderWidth * 2
        self.rect.h = rect.h + self.padding * 2 + self.borderWidth * 2

    def setStyle(self, bgColor = None, borderColor = None, padding = None, borderWidth = None, borderRadius = None):
        if bgColor:
            self.bgColor = bgColor

        if borderColor:
            self.borderColor = borderColor

        if borderRadius:
            self.borderRadius = borderRadius

        if padding:
            self.padding = padding
            self.rect.w -= self.padding * 2 - padding * 2
            self.rect.h -= self.padding * 2 - padding * 2

        if borderWidth:
            self.borderWidth = borderWidth
            self.rect.w -= self.borderWidth * 2 - borderWidth * 2
            self.rect.h -= self.borderWidth * 2 - borderWidth * 2

    def draw(self):
        pygame.draw.rect(self.win, self.borderColor, self.rect, 0, self.borderRadius)  # border
        pygame.draw.rect(self.win, self.bgColor,
                         pygame.rect.Rect(self.rect.x + self.borderWidth, self.rect.y + self.borderWidth, self.rect.w - self.borderWidth * 2, self.rect.h - self.borderWidth * 2), 0,
                         self.borderRadius)  # inner
        if self.__textSurface:
            self.win.blit(self.__textSurface,
                          pygame.rect.Rect(self.rect.x + self.borderWidth + self.padding, self.rect.y + self.borderWidth + self.padding, self.rect.w - self.borderWidth * 2, self.rect.h - self.borderWidth * 2))

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

    def onMouseEvent(self, e) -> bool:
        if not self.active:
            return False

        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                self.notifyAllActionListeners()
                return True

        return False

    def notifyAllActionListeners(self):
        for l in self.actionListeners:
            l.actionPerformed(self)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, newParent):
        self._parent = newParent

        self.rect.x, self.rect.y = self.x + newParent.rect.x + newParent.padding, self.y + newParent.rect.y + newParent.padding
