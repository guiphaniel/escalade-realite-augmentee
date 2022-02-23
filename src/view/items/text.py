import pygame

from src.utils.events.mouse_listener import MouseListener
from src.view.items.drawable import Drawable


# TODO: rajouter la gestion d'une bgImage
class Button(Drawable):
    def __init__(self, parent, x, y, text, textColor=(0, 0, 0), textSize=40, textFont="view/fonts/All the Way to the Sun.otf"):
        Drawable.__init__(self, parent, x, y, 0, 0)

        self.setText(text, textColor, textSize, textFont)

    def setText(self, text, textColor, textSize, textFont):
        font = pygame.font.SysFont(textFont, textSize)
        self.__textSurface = font.render(text, True, textColor)
        self.rect.w, self.rect.h = self.__textSurface.get_rect().topleft

    def draw(self):
        self.win.blit(self.__textSurface, self.rect)
    def update(self):
        pygame.display.update(self.rect)

