import pygame

from src.view.items.drawable import Drawable


class Handle(Drawable):
    radius = 20

    def __init__(self, x, y):
        self.id = None
        self.x = x
        self.y = y
        self.radius = 20
        self.color = (255, 255, 255)

        Drawable.__init__(self)
        self.rect = pygame.rect.Rect(x, y, self.radius * 2, self.radius * 2)

    def draw(self):
        self.rect = pygame.draw.circle(self.win, self.color, self.rect.center, self.radius)

