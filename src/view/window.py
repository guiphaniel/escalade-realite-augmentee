import pygame

from src.Singleton import Singleton
from src.view.events.event_manager import EventManager
from src.view.frames.home_frame import HomeFrame


class Window(metaclass=Singleton):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Escalade en Réalité Augmentée")
        self.win = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN, 32)
        self.eventManager = EventManager()
        #self.win = pygame.display.set_mode((400, 400))

    def __del__(self):
        pygame.quit()

    def run(self):
        homeFrame = HomeFrame()
        homeFrame.playButton.active = False
        homeFrame.repaintAll()
        self.currentFrame = homeFrame
        while self.isVisible:
            self.eventManager.catchEvent()
            self.currentFrame.execute()

    def setVisible(self, isVisible):
        self.isVisible = isVisible
        if isVisible:
            self.run()