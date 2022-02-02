import threading

import pygame

import src.view.window
from src.utils.Singleton import Singleton


class EventManager(metaclass=Singleton):
    def __init__(self):
        self.keyboardListeners = []
        self.mouseListeners = []

    def catchEvent(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                src.view.window.Window().setVisible(False)
            if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                for l in self.keyboardListeners:
                    l.onKeyboardEvent(e)
            if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
                for l in self.mouseListeners:
                    l.onMouseEvent(e)

    def addKeyboardListener(self, l):
        self.keyboardListeners.append(l)

    def removeKeyboardListener(self, l):
        self.keyboardListeners.remove(l)

    def addMouseListener(self, l):
        self.mouseListeners.append(l)

    def removeMouseListener(self, l):
        self.mouseListeners.remove(l)

    def removeAllListeners(self):
        self.keyboardListeners.clear()
        self.mouseListeners.clear()
