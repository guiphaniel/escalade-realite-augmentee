import pygame

from src.utils.events.mouse_listener import MouseListener
from src.view.items.drawable import Drawable
from src.view.items.text import Text


class ListItem(Drawable, MouseListener):
    primaryColor = (255, 255, 255)
    secondaryColor = (240, 240, 240)

    def __init__(self, obj):
        Drawable.__init__(self)
        MouseListener.__init__(self)

        self.obj = obj
        self.bgColor = self.primaryColor
        self.padding = 5
        self.w = 0
        self.h = 0
        self.rect = pygame.rect.Rect(0, 0, 0, 0)

        self.setText(obj.toString())

    def setText(self, text, textColor=(0, 0, 0), textSize=40,
                textFont="src/view/fonts/All the Way to the Sun.otf"):
        font = pygame.font.SysFont(textFont, textSize)
        self.__textSurface = font.render(text, True, textColor)
        self.w, self.h = self.rect.w, self.rect.h = self.__textSurface.get_rect().w + self.padding * 2, self.__textSurface.get_rect().h + self.padding * 2

    def draw(self):
        pygame.draw.rect(self.win, self.bgColor, self.rect)
        self.win.blit(self.__textSurface, pygame.rect.Rect(self.rect.x + self.padding, self.rect.y + self.padding, self.rect.w - self.padding * 2, self.rect.h - self.padding * 2))

    def onMouseEvent(self, e) -> bool:
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(*pygame.mouse.get_pos()):
                if self.parent.selectedItem != self:
                    self.parent.selectedItem = self
                    return True

        return False

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, newParent):
        self._parent = newParent
        if newParent:
            self.rect.x, self.rect.y = newParent.rect.x + newParent.padding, newParent.rect.y + newParent.padding