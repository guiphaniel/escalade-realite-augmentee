from collections import deque
import pygame

import src.view.window
from src.utils.Singleton import Singleton


class EventManager(metaclass=Singleton):
    def __init__(self):
        self.keyboardListeners = deque()
        self.mouseListeners = deque()
        self.motionListeners = deque()
        self.wheelListeners = deque()
        # these variables are used not to overwhelm the manager with onMotionEvent calls (will wait deltaLastMotionEvent between each)
        self.lastMotionEvent = pygame.time.get_ticks()
        self.deltaLastMotionEvent = 17

    def catchEvent(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                src.view.window.Window().setVisible(False)
                return
            elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                for l in self.keyboardListeners:
                    if l.onKeyboardEvent(e):
                        return
            elif (e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP) and (e.button == 1 or e.button == 3):
                for l in self.mouseListeners:
                    if l.onMouseEvent(e):
                        return
            elif e.type == pygame.MOUSEMOTION:
                if self.lastMotionEvent + self.deltaLastMotionEvent < pygame.time.get_ticks():
                    for l in self.motionListeners:
                        if l.onMotionEvent(e):
                            self.lastMotionEvent = pygame.time.get_ticks()
                            return
            elif (e.type == pygame.MOUSEBUTTONUP or e.type == pygame.MOUSEBUTTONDOWN) and (e.button == 4 or e.button == 5):
                for l in self.wheelListeners:
                    if l.onWheelEvent(e):
                        return

    def addKeyboardListener(self, l):
        self.keyboardListeners.appendleft(l)

    def removeKeyboardListener(self, l):
        self.keyboardListeners.remove(l)

    def addMouseListener(self, l):
        self.mouseListeners.appendleft(l)

    def removeMouseListener(self, l):
        self.mouseListeners.remove(l)

    def addMotionListener(self, l):
        self.motionListeners.appendleft(l)

    def removeMotionListener(self, l):
        self.motionListeners.remove(l)

    def addWheelListener(self, l):
        self.wheelListeners.appendleft(l)

    def removeWheelListener(self, l):
        self.wheelListeners.remove(l)

    def removeAllListeners(self):
        self.keyboardListeners.clear()
        self.mouseListeners.clear()
        self.motionListeners.clear()
        self.wheelListeners.clear()
