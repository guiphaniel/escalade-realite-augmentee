from abc import abstractmethod

from src.view.events.event_manager import EventManager


class MouseListener:
    def __init__(self):
        EventManager().addMouseListener(self)

    @abstractmethod
    def onMouseEvent(self, e):
        pass