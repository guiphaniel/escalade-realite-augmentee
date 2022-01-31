import src
from src.controllers.switch_frame_controller import SwitchFrameController
from src.view.frames.abstract_frame import AbstractFrame
from src.view.frames.calibration_frame import CalibrationFrame
from src.view.frames.games_frame import GamesFrame
from src.view.items.button import Button
from src.view.listeners.action_listener import ActionListener


class HomeFrame(AbstractFrame, ActionListener):
    def __init__(self):
        AbstractFrame.__init__(self, bgImage="view/images/background.png")
        self.calibrationButton = Button(300, 400, text="CALIBRATION")
        self.add(self.calibrationButton)
        self.playButton = Button(300, 700, text="JOUER")
        self.add(self.playButton)

        self.calibrationButton.addActionListener(self)
        self.playButton.addActionListener(self)

    def execute(self):
        pass

    # TODO: use controllers, having window imbedded
    def actionPerformed(self, source):
        if source == self.playButton:
            SwitchFrameController().control(frame=src.view.frames.home_frame.GamesFrame())
        elif source == self.calibrationButton:
            SwitchFrameController().control(frame=src.view.frames.home_frame.CalibrationFrame())
