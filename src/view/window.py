import platform

import pygame

from src.controllers.switch_frame_controller import SwitchFrameController
from src.utils.Singleton import Singleton
from src.utils.events.event_manager import EventManager
from src.view.frames.home_frame import HomeFrame


class Window(metaclass=Singleton):
    def __init__(self):
        if "windows" in platform.system().lower():
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        pygame.init()
        pygame.display.set_caption("Escalade en Réalité Augmentée")
        self.win = self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.eventManager = EventManager()
        self.currentFrame = None

    def __del__(self):
        pygame.quit()

    def run(self):
        SwitchFrameController().execute(frame=HomeFrame)
        self.currentFrame.startButton.active = False
        self.currentFrame.repaintAll()
        # self.update()
        while self.isVisible:
            self.eventManager.catchEvent()
            self.currentFrame.repaintAll()

    def setVisible(self, isVisible):
        self.isVisible = isVisible
        if isVisible:
            self.run()

    def update(self):
        self.currentFrame.repaintAll()
