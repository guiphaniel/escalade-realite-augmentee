from abc import abstractmethod

from src.view.frames.abstract_frame import AbstractFrame
from src.view.items.button import Button
from src.view.items.list import List
from src.view.listeners.action_listener import ActionListener
from src.view.listeners.list_listener import ListListener


class AbstractManagerFrame(AbstractFrame, ListListener, ActionListener):

    def __init__(self):
        AbstractFrame.__init__(self, bgImage="view/images/background.png")
        ListListener.__init__(self)
        ActionListener.__init__(self)

        self.list = List(self, 200, 200)
        self.add(self.list)
        self.addBt = Button(self, 600, 200, text="Ajouter")
        self.add(self.addBt)
        self.editBt = Button(self, 600, 400, text="Modifier")
        self.editBt.active = False
        self.add(self.editBt)
        self.removeBt = Button(self, 600, 600, text="Supprimer")
        self.removeBt.active = False
        self.add(self.removeBt)
        self.selectBt = Button(self, 600, 800, text="Selectionner")
        self.selectBt.active = False
        self.add(self.selectBt)

        self.addBt.addActionListener(self)
        self.editBt.addActionListener(self)
        self.removeBt.addActionListener(self)
        self.selectBt.addActionListener(self)

        self.list.addListListener(self)

    def actionPerformed(self, source):
        if source == self.addBt:
            self.addT()
        elif source == self.editBt:
            self.editT()
        elif source == self.removeBt:
            self.removeT()
        elif source == self.selectBt:
            self.selectT()

    @abstractmethod
    def addT(self):
        pass

    # need to update the list Items' text
    @abstractmethod
    def editT(self):
        pass

    @abstractmethod
    def removeT(self):
        pass

    # need to save in bd, and launch appropriate activity
    @abstractmethod
    def selectT(self):
        pass

    def valueChanged(self, source):
        if self.list.selectedItem:
            self.editBt.active = True
            self.removeBt.active = True
            self.selectBt.active = True
        else:
            self.editBt.active = False
            self.removeBt.active = False
            self.selectBt.active = False
