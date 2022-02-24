import pygame

from src.model.components.handle import Handle
from src.view.frames.abstract_frame import AbstractFrame


class PathFrame(AbstractFrame):
    def __init__(self):
        AbstractFrame.__init__(self)
