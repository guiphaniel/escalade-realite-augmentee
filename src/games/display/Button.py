import pygame

class Button:

    def __init__(self, surface, x,y,width,height,color,text=''):
        self.color=color
        self.text=text
        self.surface=surface
        self.rect= pygame.Rect(x,y,width,height)

    def draw(self):
        pygame.draw.rect(self.surface,self.color,self.rect)

    def pressed(self,event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(x,y):
                print("Click validé")

