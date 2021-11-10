import pygame

class Button:

    def __init__(self, surface, x,y,width,height,color,text=''):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.text=text
        self.surface=surface

    def draw(self):
        pygame.draw.rect()