import src
from src.controllers.abstract_controller import AbstractController


class SwitchFrameController(AbstractController):
    def execute(self, **kwargs):
        frame = kwargs.get("frame")
        src.view.window.Window().currentFrame = frame
        frame.repaintAll()
