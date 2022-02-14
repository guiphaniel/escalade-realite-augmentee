import threading
from abc import abstractmethod
import cv2
import numpy as np
import pygame.draw

import src
from src.controllers.abstract_controller import AbstractController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.utils.camera import Camera
from src.utils.detectors import pose_detector
from src.utils.transform import Transform
from src.utils.events.event_manager import EventManager
from src.utils.events.keyboard_listener import KeyboardListener


class Game(AbstractController, KeyboardListener):

    def __init__(self, parent):
        self.parent = parent
        self.win = src.view.window.Window().win
        EventManager().addKeyboardListener(self)
        self.continueGame = True

    def onKeyboardEvent(self, e):
        if e.key == pygame.K_ESCAPE or e.type == pygame.QUIT:
            self.continueGame = False
            SwitchFrameController().execute(frame=src.view.frames.games_frame.GamesFrame())
            return True

        return False
