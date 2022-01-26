from abc import abstractmethod

from src.view.utils.events.event_manager import EventManager


class KeyboardListener:
    def __init__(self):
        EventManager().addKeyboardListeners(self)

    def __del__(self):
        EventManager().removeKeyboardListeners(self)

    @abstractmethod
    def onKeyboardEvent(self, e):
        pass