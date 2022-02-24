import pygame

from src.view.items.drawable import Drawable


class Handle(Drawable):
    radius = 20

    def __init__(self, parent, x, y):
        self.id = None
        self.x = x
        self.y = y
        self.radius = 20

        Drawable.__init__(self, parent)
        self.rect = pygame.rect.Rect(x, y, self.radius, self.radius)

    def draw(self):
        self.rect = pygame.draw.circle(self.win, (50, 50, 50), self.rect.center, self.radius, 5)

