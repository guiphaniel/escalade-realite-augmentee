import pygame

class Button:

    def __init__(self, screen, x,y,width,height,color,text=''):
        self.text=text
        self.screen=screen
        self.surface= pygame.Surface((width,height))
        self.rect=self.surface.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.surface.fill(color)
        self.font = pygame.font.Font('freesansbold.ttf',16)

    def draw(self):
        if self.text!='':
            render=self.font.render(self.text,True,(255,255,255),(255,0,0,0))
            self.screen.blit(render,self.rect)

    def pressed(self,event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(x,y):
                self.rect.move_ip(10,10)
                print("Click validé")

