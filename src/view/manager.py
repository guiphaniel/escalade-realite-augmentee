import threading
import pygame
import ctypes
from src.view.utils.buttons.calibration_button import CalibrationButton
from src.view.utils.buttons.handle_detection_button import HandleDetectorButton
from src.view.utils.buttons.osu_button import OsuButton
from src.view.utils.buttons.parcours_button import ParcoursButton
from src.view.utils.buttons.play_button import PlayButton
from src.view.utils.buttons.pong_button import PongButton
from src.view.utils.buttons.return_button import ReturnButton


class Manager(threading.Thread):

    def __init__(self, width, height):
        threading.Thread.__init__(self)
        self.width = width
        self.height = height
        self.wallCalibration=None
        self.screen = None
        self.gameMenu = False
        self.running = True
        self.background = pygame.image.load("view/images/background.png")

    def run(self):
        ctypes.windll.user32.SetProcessDPIAware()
        pygame.init()
        pygame.display.set_caption("Escalade en Réalité Augmentée")
        self.screen = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN,32)

        buttons = [PlayButton(self, "view/images/jouer.png", 300, 700),
                   CalibrationButton(self, "view/images/calibration.png", 300, 400)]
        while self.running:
            self.screen.blit(self.background,(0,0))
            for b in buttons:
                self.screen.blit(b.image, b.rect)
            pygame.display.flip()  # Met à jour l'écran
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for b in buttons:
                        if b.rect.collidepoint(x, y):
                            b.pressed()
        pygame.quit()

    def startMenuGame(self):

        buttons = [OsuButton(self,"view/images/osu.png",300,400),
                   ParcoursButton(self,"view/images/parcours.png",300,700),
                   PongButton(self,"view/images/pong.png",300,100),
                   ReturnButton(self,"view/images/retour.png",1551,919),
                   #HandleDetectorButton(self,"view/images/detection.png", 900,550)
                   ]

        self.gameMenu = True
        while self.gameMenu:
            self.screen.blit(self.background, (0, 0))
            for b in buttons:
                self.screen.blit(b.image, b.rect)
            pygame.display.flip()  # Met à jour l'écran
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.gameMenu = False
                if e.type == pygame.QUIT:
                    self.gameMenu = False
                    self.running= False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for b in buttons:
                        if b.rect.collidepoint(x, y):
                            b.pressed()

