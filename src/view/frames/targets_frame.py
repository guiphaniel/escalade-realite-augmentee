from src.games.osu_game import OsuGame
from src.view.frames.abstract_frame import AbstractFrame
from src.view.items.button import Button
from src.view.listeners.action_listener import ActionListener


class TargetsFrame(AbstractFrame, ActionListener):
    def __init__(self):
        AbstractFrame.__init__(self)

        self.targetGame = OsuGame()

    def execute(self):
        self.targetGame.execute()

    # TODO: use controllers, having window imbedded
    def actionPerformed(self, src):
        pass
