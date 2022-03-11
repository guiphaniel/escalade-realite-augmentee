from enum import Enum

import pygame

from src.controllers.games.path_game import PathGame
from src.controllers.start_game_controller import StartGameController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.model.components.handle import Handle
from src.model.components.player import Player
from src.model.database import Database
from src.utils.events.keyboard_listener import KeyboardListener
from src.view.frames.path_frame import PathFrame
from src.view.internalframes.AbstractInternalFrame import AbstractInternalFrame
from src.view.items.button import Button
from src.view.items.edit_text import EditText
from src.view.listeners.action_listener import ActionListener


class PathEditor(AbstractInternalFrame, ActionListener, KeyboardListener):

    class EditorMode(Enum):
        ADD = 0
        REMOVE = 1
        EDIT = 2

    def __init__(self, path, coordinates, bgColor = (50, 50, 50), bgImage = None):
        AbstractInternalFrame.__init__(self, coordinates, bgColor, bgImage)
        ActionListener.__init__(self)
        KeyboardListener.__init__(self)
        self.path = path
        self.handles = Database().getHandlesInPath(path)
        self.editorMode = self.EditorMode.ADD
        self.lastMousePosX = None
        self.lastMousePosY = None
        self.editedHandle = None

        self.editText = EditText(0, 0, self.path.name)
        self.add(self.editText)
        self.addBt = Button(0, self.editText.rect.h + 20, 10, 10, text=" + ")
        self.addBt.setStyle(borderRadius=100)
        self.add(self.addBt)
        self.removeBt = Button(self.addBt.rect.x + self.addBt.rect.w + 40, self.editText.rect.h + 20, text=" - ")
        self.removeBt.setStyle(borderRadius=100)
        self.add(self.removeBt)
        self.editBt = Button(self.removeBt.rect.x + self.removeBt.rect.w + 40, self.editText.rect.h + 20, text=" / ")
        self.editBt.setStyle(borderRadius=100)
        self.add(self.editBt)
        self.backBt = Button(0, self.editBt.rect.y + self.editBt.rect.h + 20, text="RETOUR")
        self.add(self.backBt)
        self.validBt = Button(self.backBt.rect.w + 20, self.editBt.rect.y + self.editBt.rect.h + 20, text="VALIDER")
        self.__isHandlesEmpty()
        self.add(self.validBt)

        self.shrinkToFit()

        self.addBt.addActionListener(self)
        self.removeBt.addActionListener(self)
        self.editBt.addActionListener(self)
        self.backBt.addActionListener(self)
        self.validBt.addActionListener(self)

    def actionPerformed(self, source):
        if source == self.addBt:
            self.editorMode = self.EditorMode.ADD
        elif source == self.removeBt:
            self.editorMode = self.EditorMode.REMOVE
        elif source == self.editBt:
            self.editorMode = self.EditorMode.EDIT
        elif source == self.backBt:
            from src.view.frames.path_manager_frame import PathManagerFrame
            SwitchFrameController().execute(frame=PathManagerFrame)
        elif source == self.validBt:
            self.__onValid()

    def __onValid(self):
        self.path.setHandles(self.handles)
        Database().setHandlesInPath(self.handles, self.path)
        self.path.name = self.editText.text
        Database().updatePath(self.path)
        from src.view.frames.path_manager_frame import PathManagerFrame
        SwitchFrameController().execute(frame=PathManagerFrame)

    def onMouse(self, e) -> bool:
        pos = pygame.mouse.get_pos()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.editorMode == self.EditorMode.ADD:
                handle = Handle(pos[0] - Handle.radius / 2, pos[1] - Handle.radius / 2)
                self.handles.append(handle)
                self.parent.add(handle)
                self.__isHandlesEmpty()
                return True

            elif self.editorMode == self.EditorMode.REMOVE:
                handle = self.__findHandle(pygame.mouse.get_pos())
                if handle:
                    self.handles.remove(handle)
                    self.parent.remove(handle)
                    self.__isHandlesEmpty()
                    return True

        if self.editorMode == self.EditorMode.EDIT:
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.lastMousePosX, self.lastMousePosY = pos
                self.editedHandle = self.__findHandle(pos)
            if e.type == pygame.MOUSEBUTTONUP:
                self.editedHandle = None
            return True

        return False

    def __findHandle(self, coordinates):
        for h in self.handles:
            if h.rect.collidepoint(coordinates):
                return h

    def __isHandlesEmpty(self):
        if self.handles:
            self.validBt.active = True
        else:
            self.validBt.active = False

    def onMotion(self, e) -> bool:
        if self.editedHandle:
            x, y = pygame.mouse.get_pos()
            newX, newY = x - self.lastMousePosX, y - self.lastMousePosY
            self.lastMousePosX, self.lastMousePosY = x, y

            self.editedHandle.move(newX, newY)
            return True

        return False

    def onKeyboardEvent(self, e) -> bool:
        if e.type == pygame.KEYDOWN and (e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER):
            self.__onValid()
            return True

        return False

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, newParent):
        self._parent = newParent
        for h in self.handles:
            h.parent = self.parent
            self.parent.add(h)
