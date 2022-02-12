import pygame

from src.view.internalframes.AbstractInternalFrame import AbstractInternalFrame
from src.view.items.button import Button


class HandleEditorInternalFrame(AbstractInternalFrame):
    def __init__(self, parent, coordinates, bgColor = (50, 50, 50), bgImage = None):
        super().__init__(parent, coordinates, bgColor, bgImage)

        self.addBt = Button(self, 0, 0, 10, 10, text=" + ")
        self.addBt.setStyle(borderRadius=100)
        self.add(self.addBt)
        self.removeBt = Button(self, self.addBt.rect.x + self.addBt.rect.w + 20, 0, text=" - ")
        self.removeBt.setStyle(borderRadius=100)
        self.add(self.removeBt)
        self.editBt = Button(self, self.removeBt.rect.x + self.removeBt.rect.w + 20, 0, text=" / ")
        self.editBt.setStyle(borderRadius=100)
        self.add(self.editBt)

        self.shrinkToFit()