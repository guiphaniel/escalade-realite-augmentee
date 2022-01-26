import threading

import pygame

from src.Singleton import Singleton
from src.view.utils.events.event_manager import EventManager
from src.view.utils.frames.home_frame import HomeFrame


class Window(metaclass=Singleton):
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((200, 200))

    def __del__(self):
        EventManager().stop()
        pygame.quit()

    def run(self):
        self.currentFrame = HomeFrame(bgImage="view/images/background.png")
        while self.isVisible:
            EventManager().catchEvent()
            self.currentFrame.execute()

    def setVisible(self, isVisible):
        self.isVisible = isVisible
        if isVisible:
            self.run()
