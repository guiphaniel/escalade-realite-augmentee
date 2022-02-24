from enum import Enum

import pygame

from src.view.internalframes.AbstractInternalFrame import AbstractInternalFrame
from src.view.items.button import Button
from src.view.listeners.action_listener import ActionListener


class HandleEditorInternalFrame(AbstractInternalFrame, ActionListener):
    class EditorMode(Enum):
        ADD = 0
        REMOVE = 1
        EDIT = 2

    def __init__(self, parent, coordinates, bgColor = (50, 50, 50), bgImage = None):
        super().__init__(parent, coordinates, bgColor, bgImage)

        self.addBt = Button(self, 0, 0, 10, 10, text=" + ")
        self.addBt.setStyle(borderRadius=100)
        self.add(self.addBt)
        self.removeBt = Button(self, self.addBt.rect.x + self.addBt.rect.w + 40, 0, text=" - ")
        self.removeBt.setStyle(borderRadius=100)
        self.add(self.removeBt)
        self.editBt = Button(self, self.removeBt.rect.x + self.removeBt.rect.w + 40, 0, text=" / ")
        self.editBt.setStyle(borderRadius=100)
        self.add(self.editBt)
        self.backBt = Button(self, 0, self.editBt.rect.h + 20, text="RETOUR")
        self.add(self.backBt)
        self.validBt = Button(self, self.backBt.rect.w + 20, self.editBt.rect.h + 20, text="VALIDER")
        self.add(self.validBt)

        self.shrinkToFit()

        self.addBt.addActionListener(self)
        self.removeBt.addActionListener(self)
        self.editBt.addActionListener(self)
        self.backBt.addActionListener(self)
        self.validBt.addActionListener(self)

    def actionPerformed(self, source):
        if source == self.addBt:
            self.parent.editorMode = self.EditorMode.ADD
        elif source == self.removeBt:
            self.parent.editorMode = self.EditorMode.REMOVE
        elif source == self.editBt:
            self.parent.editorMode = self.EditorMode.EDIT
        elif source == self.backBt:
            self.parent.onBackBt()
        elif source == self.validBt:
            self.parent.onValidBt()
