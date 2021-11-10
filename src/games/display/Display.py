import threading
import multiprocessing as mp
class Display():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        p = mp.Process(target=self.run)
        print("run")
        p.start()

    def run(self):
        import pygame
        pygame.init()
        pygame.display.set_caption("Escalade en Réalité Augmentée")
        pygame.display.set_mode((self.width, self.height))
        running=True

        while running:

            pygame.display.flip() #Met à jour l'écran

            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    running=False
                    pygame.quit()