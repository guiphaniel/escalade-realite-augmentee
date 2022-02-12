from abc import abstractmethod

from src.utils.events.event_manager import EventManager


class KeyboardListener:
    def __init__(self):
        EventManager().addKeyboardListeners(self)

    #needs to return True if the event is caught (i.e. the element is concerned by the event)
    @abstractmethod
    def onKeyboardEvent(self, e) -> bool:
        pass