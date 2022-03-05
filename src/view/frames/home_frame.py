import pygame

import src
from src.controllers.start_calibration_controller import StartCalibrationController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.view.frames.abstract_frame import AbstractFrame
from src.view.frames.calibration_frame import CalibrationFrame
from src.view.frames.games_frame import GamesFrame
from src.view.items.button import Button
from src.view.listeners.action_listener import ActionListener


class HomeFrame(AbstractFrame, ActionListener):
    def __init__(self):
        AbstractFrame.__init__(self, bgImage="view/images/background.png")
        self.calibrationButton = Button(self, 300, 100, text="CALIBRER")
        self.add(self.calibrationButton)
        self.startButton = Button(self, 300, 400, text="COMMENCER")
        self.add(self.startButton)
        self.quitButton = Button(self, 1551, 919, text="QUITTER")
        self.add(self.quitButton)

        self.calibrationButton.addActionListener(self)
        self.startButton.addActionListener(self)
        self.quitButton.addActionListener(self)

    # TODO: use controllers, having window imbedded
    def actionPerformed(self, source):
        if source == self.startButton:
            SwitchFrameController().execute(frame=src.view.frames.home_frame.GamesFrame())
        elif source == self.calibrationButton:
            SwitchFrameController().execute(frame=src.view.frames.home_frame.CalibrationFrame())
            StartCalibrationController().execute()
        elif source == self.quitButton:
            from src.view.window import Window
            Window().setVisible(False)
