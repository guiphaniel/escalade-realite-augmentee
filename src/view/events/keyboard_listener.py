from abc import abstractmethod

from src.view.events.event_manager import EventManager


class KeyboardListener:
    def __init__(self):
        EventManager().addKeyboardListeners(self)

    @abstractmethod
    def onKeyboardEvent(self, e):
        pass