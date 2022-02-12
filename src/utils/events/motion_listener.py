from abc import abstractmethod

from src.utils.events.event_manager import EventManager


class MotionListener:
    def __init__(self):
        EventManager().addMotionListener(self)

    #needs to return True if the event is caught (i.e. the element is concerned by the event)
    @abstractmethod
    def onMotionEvent(self, e) -> bool:
        pass