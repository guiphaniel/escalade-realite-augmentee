import pygame

import src
from src.controllers.start_calibration_controller import StartCalibrationController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.utils.events.keyboard_listener import KeyboardListener
from src.view.frames.abstract_frame import AbstractFrame
from src.view.frames.calibration_frame import CalibrationFrame
from src.view.frames.games_frame import GamesFrame
from src.view.items.button import Button
from src.view.listeners.action_listener import ActionListener


class HomeFrame(AbstractFrame, ActionListener, KeyboardListener):
    def __init__(self):
        AbstractFrame.__init__(self, bgImage="view/images/background.png")
        ActionListener.__init__(self)
        KeyboardListener.__init__(self)
        self.calibrationButton = Button(300, 100, text="CALIBRER")
        self.add(self.calibrationButton)
        self.startButton = Button(300, 400, text="COMMENCER")
        self.add(self.startButton)
        self.quitButton = Button(1551, 919, text="QUITTER")
        self.add(self.quitButton)

        self.calibrationButton.addActionListener(self)
        self.startButton.addActionListener(self)
        self.quitButton.addActionListener(self)

    def actionPerformed(self, source):
        if source == self.startButton:
            SwitchFrameController().execute(frame=src.view.frames.home_frame.GamesFrame)
        elif source == self.calibrationButton:
            SwitchFrameController().execute(frame=src.view.frames.home_frame.CalibrationFrame)
            StartCalibrationController().execute()
        elif source == self.quitButton:
            self.__onQuit()

    def __onQuit(self):
        from src.view.window import Window
        Window().setVisible(False)

    def onKeyboardEvent(self, e) -> bool:
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.__onQuit()
            return True

        return False
