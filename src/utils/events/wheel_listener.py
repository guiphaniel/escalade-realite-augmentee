from abc import abstractmethod

from src.utils.events.event_manager import EventManager


class WheelListener:
    def __init__(self):
        EventManager().addWheelListener(self)

    #needs to return True if the event is caught (i.e. the element is concerned by the event)
    @abstractmethod
    def onWheelEvent(self, e) -> bool:
        pass