import pygame

from src.view.items.drawable import Drawable

# TODO: rajouter la gestion d'une bgImage
from src.view.items.item_display_type import ItemDisplayType


class Text(Drawable):
    def __init__(self, x, y, text, textColor=(255, 255, 255), textSize=40,
                 textFont="view/fonts/All the Way to the Sun.otf", displayType=ItemDisplayType.TOP_LEFT):
        Drawable.__init__(self, displayType)

        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(0, 0, 0, 0)

        self.setText(text, textColor, textSize, textFont)

    def setText(self, text, textColor=(0, 0, 0), textSize=40,
                textFont="view/fonts/All the Way to the Sun.otf"):
        font = pygame.font.SysFont(textFont, textSize)
        self.__textSurface = font.render(text, True, textColor)
        self.rect.w, self.rect.h = self.__textSurface.get_rect().w, self.__textSurface.get_rect().h

        if self.displayType == ItemDisplayType.CENTER:
            self.rect.x, self.rect.y = self.x - self.rect.w / 2, self.y - self.rect.h / 2

    def draw(self):
        self.win.blit(self.__textSurface, self.rect)

    def update(self):
        pygame.display.update(self.rect)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, newParent):
        self._parent = newParent
        self.rect.x, self.rect.y = self.x + newParent.rect.x + newParent.padding, self.y + newParent.rect.y + newParent.padding
