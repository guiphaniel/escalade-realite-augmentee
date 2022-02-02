from abc import abstractmethod

from src.view.events.event_manager import EventManager


class MouseListener:
    def __init__(self):
        EventManager().addMouseListener(self)

    #needs to return True if the event is caught (i.e. the element is concerned by the event)
    @abstractmethod
    def onMouseEvent(self, e) -> bool:
        pass