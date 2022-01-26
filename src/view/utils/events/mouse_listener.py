from abc import abstractmethod

from src.view.utils.events.event_manager import EventManager


class MouseListener:
    def __init__(self):
        EventManager().addMouseListener(self)

    def __del__(self):
        EventManager().removeMouseListener(self)

    @abstractmethod
    def onMouseEvent(self, e):
        pass