import threading

import src
from src.controllers.abstract_controller import AbstractController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.utils.transform import Transform


class StartCalibrationController(AbstractController):
    def execute(self, **kwargs):
        if Transform().startCalibration():
            SwitchFrameController().execute(frame=src.view.frames.home_frame.HomeFrame())
        else:
            homeFrame = src.view.frames.home_frame.HomeFrame()
            homeFrame.startButton.active = False
            SwitchFrameController().execute(frame=homeFrame)
