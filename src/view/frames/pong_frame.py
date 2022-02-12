from src.controllers.games.pong_game import PongGame
from src.view.frames.abstract_frame import AbstractFrame


class PongFrame(AbstractFrame):
    def __init__(self):
        AbstractFrame.__init__(self)