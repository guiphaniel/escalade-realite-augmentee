import pygame

from src.utils.events.mouse_listener import MouseListener
from src.view.items.drawable import Drawable


# TODO: rajouter la gestion d'une bgImage
class Rectangle(Drawable):
    def __init__(self, parent, x, y, w=40, h=20, bgColor = (255, 255, 255)):
        Drawable.__init__(self, parent)

        # init textures
        self.bgColor = bgColor

        # self.rect is equivalent to the outer rect of the button (margin + borders included)
        self.rect = pygame.rect.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(self.win, self.bgColor, self.rect)

    def update(self):
        pygame.display.update(self.rect)

