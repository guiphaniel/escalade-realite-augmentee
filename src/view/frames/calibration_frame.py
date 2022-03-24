import pygame

import src
from src.controllers.switch_frame_controller import SwitchFrameController
from src.utils.transform import Transform
from src.view.frames.abstract_frame import AbstractFrame


class CalibrationFrame(AbstractFrame):
    def __init__(self):
        AbstractFrame.__init__(self, bgImage="./src/view/images/charucoboard.jpg")

