import pygame

from src.utils.events.keyboard_listener import KeyboardListener
from src.view.items.drawable import Drawable
from src.view.items.text import Text


class EditText(Drawable, KeyboardListener):

    def __init__(self, parent, x, y, text):
        Drawable.__init__(self, parent)
        KeyboardListener.__init__(self)
        self.bgColor = (255, 255, 255)
        self.padding = 5
        self.rect = pygame.rect.Rect(parent.rect.x + parent.padding, parent.rect.y + parent.padding, 0, 0)

        self.initialText = text
        self.text = text

        self.setText(self.text)

    def setText(self, text, textColor=(0, 0, 0), textSize=40,
                textFont="view/fonts/All the Way to the Sun.otf"):
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
            return True

        return False