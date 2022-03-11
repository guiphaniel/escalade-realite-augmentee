from abc import abstractmethod

import pygame.draw

import src
from src.controllers.abstract_controller import AbstractController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.utils.events.keyboard_listener import KeyboardListener


class Game(AbstractController, KeyboardListener):

    def __init__(self, parent):
        KeyboardListener.__init__(self)
        self.parent = parent
        self.win = src.view.window.Window().win
        self.continueGame = True

    def onKeyboardEvent(self, e):
        if e.key == pygame.K_ESCAPE or e.type == pygame.QUIT:
            self.continueGame = False
            SwitchFrameController().execute(frame=src.view.frames.games_frame.GamesFrame)
            return True

        return False

    @abstractmethod
    def execute(self):
        pass