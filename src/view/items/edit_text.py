import pygame

from src.utils.events.keyboard_listener import KeyboardListener
from src.view.items.drawable import Drawable
from src.view.items.text import Text


class EditText(Drawable, KeyboardListener):

    def __init__(self, x, y, text):
        Drawable.__init__(self)
        KeyboardListener.__init__(self)
        self.bgColor = (255, 255, 255)
        self.padding = 5
        self.rect = pygame.rect.Rect(x, y, 0, 0)

        self.initialText = text
        self.text = text

        self.setText(self.text)

    def setText(self, text, textColor=(0, 0, 0), textSize=40,
                textFont="src/view/fonts/All the Way to the Sun.otf"):
        font = pygame.font.SysFont(textFont, textSize)
        self.__textSurface = font.render(text, True, textColor)
        self.rect.w, self.rect.h = self.__textSurface.get_rect().w + self.padding * 2, self.__textSurface.get_rect().h + self.padding * 2


    def draw(self):
        pygame.draw.rect(self.win, self.bgColor, self.rect)
        self.win.blit(self.__textSurface, pygame.rect.Rect(self.rect.x + self.padding, self.rect.y + self.padding,
                                                           self.rect.w - self.padding * 2,
                                                           self.rect.h - self.padding * 2))

    def onKeyboardEvent(self, e) -> bool:
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER or e.key == pygame.K_ESCAPE:
                return False
            else:
                self.text += e.unicode

            self.setText(self.text)
            self.parent.shrinkToFit()
            # from src.view.window import Window
            # Window().update()
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