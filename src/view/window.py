import ctypes

import pygame

from src.controllers.switch_frame_controller import SwitchFrameController
from src.utils.Singleton import Singleton
from src.utils.events.event_manager import EventManager
from src.view.frames.home_frame import HomeFrame


class Window(metaclass=Singleton):
    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware()
        pygame.init()
        pygame.display.set_caption("Escalade en Réalité Augmentée")
        self.win = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN, 32)
        self.eventManager = EventManager()
        self.currentFrame = None
        #self.win = pygame.display.set_mode((400, 400))

    def __del__(self):
        pygame.quit()

    def run(self):
        SwitchFrameController().execute(frame=HomeFrame)
        # homeFrame.startButton.active = False
        while self.isVisible:
            self.eventManager.catchEvent()
            self.currentFrame.repaintAll()

    def setVisible(self, isVisible):
        self.isVisible = isVisible
        if isVisible:
            self.run()
