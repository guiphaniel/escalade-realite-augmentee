import threading
import pygame

from src.games.display.Button import Button


class Display(threading.Thread):

    def __init__(self, width, height):
        threading.Thread.__init__(self)
        self.width = width
        self.height = height

    def run(self):
        threading.Thread.__init__(self)
        print("run")
        pygame.init()
        pygame.display.set_caption("Escalade en Réalité Augmentée")
        screen = pygame.display.set_mode((self.width, self.height))
        running=True
        red = (255,0,0)
        i=10.0
        button = Button(screen,i,i,50,20,red,"Calibration")
        while running:
            screen.fill((0,0,0,0))
            button.draw()
            pygame.display.flip() #Met à jour l'écran
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    running=False
                    pygame.quit()
                button.pressed(e)