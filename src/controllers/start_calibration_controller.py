import threading

import src
from src.controllers.abstract_controller import AbstractController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.utils.transform import Transform


class StartCalibrationController(AbstractController):
    def execute(self, **kwargs):
        if Transform().startCalibration():
            SwitchFrameController().execute(frame=src.view.frames.home_frame.HomeFrame)
        else:
            SwitchFrameController().execute(frame=src.view.frames.home_frame.HomeFrame)
            from src.view.window import Window
            Window().currentFrame.startButton.active = False
            Window().update()
