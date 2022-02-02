from src.controllers.games.osu_game import OsuGame
from src.controllers.games.pong_game import PongGame
from src.view.frames.abstract_frame import AbstractFrame
from src.view.listeners.action_listener import ActionListener


class PongFrame(AbstractFrame):
    def __init__(self):
        AbstractFrame.__init__(self)

        self.pongGame = PongGame()

    def execute(self):
        self.pongGame.execute()
