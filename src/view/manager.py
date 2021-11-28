import threading
import pygame

from src.view.utils.buttons.calibration_button import calibrationButton
from src.view.utils.buttons.play_button import playButton


class Manager(threading.Thread):

    def __init__(self, width, height):
        threading.Thread.__init__(self)
        self.width = width
        self.height = height

    def run(self):
        pygame.init()
        pygame.display.set_caption("Escalade en Réalité Augmentée")
        screen = pygame.display.set_mode((960, 540))
        running = True
        buttons = [playButton(screen, "view/images/jouer.png", 300, 200),
                   calibrationButton(screen, "view/images/calibration.png", 300, 400)]
        while running:
            screen.fill((0, 0, 0, 0))
            for b in buttons:
                screen.blit(b.image, b.rect)
            pygame.display.flip()  # Met à jour l'écran
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for b in buttons:
                        if b.rect.collidepoint(x, y):
                            b.pressed()
