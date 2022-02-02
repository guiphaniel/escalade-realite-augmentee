from src.controllers.games.osu_game import OsuGame
from src.view.frames.abstract_frame import AbstractFrame
from src.view.listeners.action_listener import ActionListener


class TargetsFrame(AbstractFrame):
    def __init__(self):
        AbstractFrame.__init__(self)

        self.targetGame = OsuGame()

    def execute(self):
        self.targetGame.execute()
