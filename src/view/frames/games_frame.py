import src
from src.controllers.games.targets_game import TargetsGame
from src.controllers.games.path_game import PathGame
from src.controllers.games.pong_game import PongGame
from src.controllers.start_game_controller import StartGameController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.model.components.path import Path
from src.model.database import Database
from src.view.frames.abstract_frame import AbstractFrame
from src.view.frames.path_creation_frame import PathCreationFrame
from src.view.frames.path_frame import PathFrame
from src.view.frames.path_manager_frame import PathManagerFrame
from src.view.frames.targets_frame import TargetsFrame
from src.view.items.button import Button
from src.view.listeners.action_listener import ActionListener
from src.view.frames.pong_frame import PongFrame

class GamesFrame(AbstractFrame, ActionListener):
    def __init__(self):
        AbstractFrame.__init__(self, bgImage="view/images/background.png")
        self.pongButton = Button(self, 300, 100, text="PONG")
        self.add(self.pongButton)
        self.targetButton = Button(self, 300, 400, text="CIBLES")
        self.add(self.targetButton)
        self.pathButton = Button(self, 300, 700, text="PARCOURS")
        self.add(self.pathButton)
        self.returnButton = Button(self, 1551, 919, text="RETOUR")
        self.add(self.returnButton)

        self.pongButton.addActionListener(self)
        self.targetButton.addActionListener(self)
        self.pathButton.addActionListener(self)
        self.returnButton.addActionListener(self)

    #TODO: use controllers, having window imbedded
    def actionPerformed(self, source):
        if source == self.pongButton:
            pongFrame = PongFrame()
            SwitchFrameController().execute(frame=pongFrame)
            StartGameController().execute(game=PongGame(pongFrame))
        elif source == self.targetButton:
            targetFrame = TargetsFrame()
            SwitchFrameController().execute(frame=targetFrame)
            StartGameController().execute(game=TargetsGame(targetFrame))
        elif source == self.pathButton:
            SwitchFrameController().execute(frame=PathManagerFrame())
        elif source == self.returnButton:
            from src.view.frames.home_frame import HomeFrame
            SwitchFrameController().execute(frame=HomeFrame())
