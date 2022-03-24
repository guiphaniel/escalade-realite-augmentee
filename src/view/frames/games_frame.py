import pygame

import src
from src.controllers.games.targets_game import TargetsGame
from src.controllers.games.path_game import PathGame
from src.controllers.games.pong_game import PongGame
from src.controllers.start_game_controller import StartGameController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.model.components.path import Path
from src.model.database import Database
from src.utils.events.keyboard_listener import KeyboardListener
from src.view.frames.abstract_frame import AbstractFrame
from src.view.frames.path_creation_frame import PathCreationFrame
from src.view.frames.path_frame import PathFrame
from src.view.frames.path_manager_frame import PathManagerFrame
from src.view.frames.targets_frame import TargetsFrame
from src.view.items.button import Button
from src.view.listeners.action_listener import ActionListener
from src.view.frames.pong_frame import PongFrame


class GamesFrame(AbstractFrame, ActionListener, KeyboardListener):
    def __init__(self):
        AbstractFrame.__init__(self, bgImage="./src/view/images/background.png")
        ActionListener.__init__(self)
        KeyboardListener.__init__(self)
        self.pongButton = Button(300, 100, text="PONG")
        self.add(self.pongButton)
        self.targetButton = Button(300, 400, text="CIBLES")
        self.add(self.targetButton)
        self.pathButton = Button(300, 700, text="PARCOURS")
        self.add(self.pathButton)
        self.scoresButton = Button(1551, 100, text="SCORES")
        self.add(self.scoresButton)
        self.returnButton = Button(1551, 919, text="RETOUR")
        self.add(self.returnButton)

        self.pongButton.addActionListener(self)
        self.targetButton.addActionListener(self)
        self.pathButton.addActionListener(self)
        self.scoresButton.addActionListener(self)
        self.returnButton.addActionListener(self)

    def actionPerformed(self, source):
        if source == self.pongButton:
            SwitchFrameController().execute(frame=PongFrame)
            StartGameController().execute(game=PongGame())
        elif source == self.targetButton:
            SwitchFrameController().execute(frame=TargetsFrame)
            StartGameController().execute(game=TargetsGame())
        elif source == self.pathButton:
            SwitchFrameController().execute(frame=PathManagerFrame)
        elif source == self.returnButton:
            self.__onBack()
        elif source == self.scoresButton:
            from src.view.frames.scores_frame import ScoresFrame
            SwitchFrameController().execute(frame=ScoresFrame)

    def __onBack(self):
        from src.view.frames.home_frame import HomeFrame
        SwitchFrameController().execute(frame=HomeFrame)

    def onKeyboardEvent(self, e) -> bool:
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.__onBack()
            return True

        return False
