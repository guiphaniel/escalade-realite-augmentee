import threading

import pygame

import src.view.window
from src.utils.Singleton import Singleton


class EventManager(metaclass=Singleton):
    def __init__(self):
        self.keyboardListeners = []
        self.mouseListeners = []
        self.motionListeners = []
        # these variables are used not to overwhelm the manager with onMotionEvent calls (will wait deltaLastMotionEvent between each)
        self.lastMotionEvent = pygame.time.get_ticks()
        self.deltaLastMotionEvent = 17

    def catchEvent(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                src.view.window.Window().setVisible(False)
                return
            if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                for l in self.keyboardListeners:
                    if l.onKeyboardEvent(e):
                        return
            if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
                for l in self.mouseListeners:
                    if l.onMouseEvent(e):
                        return
            if e.type == pygame.MOUSEMOTION:
                if self.lastMotionEvent + self.deltaLastMotionEvent < pygame.time.get_ticks():
                    for l in self.motionListeners:
                        if l.onMotionEvent(e):
                            self.lastMotionEvent = pygame.time.get_ticks()
                            return

    def addKeyboardListener(self, l):
        self.keyboardListeners.append(l)

    def removeKeyboardListener(self, l):
        self.keyboardListeners.remove(l)

    def addMouseListener(self, l):
        self.mouseListeners.append(l)

    def removeMouseListener(self, l):
        self.mouseListeners.remove(l)

    def addMotionListener(self, l):
        self.motionListeners.append(l)

    def removeMotionListener(self, l):
        self.motionListeners.remove(l)

    def removeAllListeners(self):
        self.keyboardListeners.clear()
        self.mouseListeners.clear()
