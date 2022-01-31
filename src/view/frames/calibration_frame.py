import pygame

import src
from src.controllers.switch_frame_controller import SwitchFrameController
from src.utils.transform import Transform
from src.view.frames.abstract_frame import AbstractFrame


class CalibrationFrame(AbstractFrame):
    def __init__(self):
        AbstractFrame.__init__(self, bgImage="view/images/charucoboard.jpg")

    def execute(self):
        if Transform().startCalibration():
            SwitchFrameController().control(frame=src.view.frames.home_frame.HomeFrame())
        else:
            homeFrame = src.view.frames.home_frame.HomeFrame()
            homeFrame.playButton.active = False
            homeFrame.repaintAll()
            SwitchFrameController().control(frame=homeFrame)
