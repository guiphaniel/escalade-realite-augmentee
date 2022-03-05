from src.controllers.games.targets_game import TargetsGame
from src.view.frames.abstract_frame import AbstractFrame
from src.view.listeners.action_listener import ActionListener


class TargetsFrame(AbstractFrame):
    def __init__(self, bgColor = (0, 0, 0), bgImage = None):
        AbstractFrame.__init__(self, bgColor, bgImage)
