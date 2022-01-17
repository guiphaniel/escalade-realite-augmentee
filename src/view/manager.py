import threading
import pygame
import ctypes
from src.view.utils.buttons.calibration_button import calibrationButton
from src.view.utils.buttons.osu_button import OsuButton
from src.view.utils.buttons.parcours_button import ParcoursButton
from src.view.utils.buttons.play_button import playButton


class Manager(threading.Thread):

    def __init__(self, width, height):
        threading.Thread.__init__(self)
        self.width = width
        self.height = height
        self.wallCalibration=None
        self.screen = None

    def run(self):
        ctypes.windll.user32.SetProcessDPIAware()
        pygame.init()
        pygame.display.set_caption("Escalade en Réalité Augmentée")
        self.screen = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN,32)

        running = True
        background = pygame.image.load("view/images/background.png")
        buttons = [playButton(self, "view/images/jouer.png", 300, 700),
                   calibrationButton(self, "view/images/calibration.png", 300, 400)]
        while running:
            self.screen.blit(background,(0,0))
            for b in buttons:
                self.screen.blit(b.image, b.rect)
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

    def startMenuGame(self):
        background = pygame.image.load("view/images/background.png")

        buttons = [OsuButton(self,"view/images/osu.png",300,400),
                   ParcoursButton(self,"view/images/parcours.png",300,700)]

        running = True
        while running:
            self.screen.blit(background, (0, 0))
            for b in buttons:
                self.screen.blit(b.image, b.rect)
            pygame.display.flip()  # Met à jour l'écran
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        running = False
                if e.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for b in buttons:
                        if b.rect.collidepoint(x, y):
                            b.pressed()