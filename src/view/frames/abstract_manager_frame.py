from abc import abstractmethod

from src.view.frames.abstract_frame import AbstractFrame
from src.view.items.button import Button
from src.view.items.list import List
from src.view.listeners.action_listener import ActionListener
from src.view.listeners.list_listener import ListListener


class AbstractManagerFrame(AbstractFrame, ListListener, ActionListener):

    def __init__(self):
        AbstractFrame.__init__(self, bgImage="src/view/images/background.png")
        ListListener.__init__(self)
        ActionListener.__init__(self)

        self.list = List(200, 200)
        self.add(self.list)
        self.addBt = Button(600, 200, text="Ajouter")
        self.add(self.addBt)
        self.editBt = Button(600, 400, text="Modifier")
        self.editBt.active = False
        self.add(self.editBt)
        self.removeBt = Button(600, 600, text="Supprimer")
        self.removeBt.active = False
        self.add(self.removeBt)
        self.selectBt = Button(600, 800, text="Selectionner")
        self.selectBt.active = False
        self.add(self.selectBt)
        self.backBt = Button(1551, 919, text="RETOUR")
        self.add(self.backBt)

        self.addBt.addActionListener(self)
        self.editBt.addActionListener(self)
        self.removeBt.addActionListener(self)
        self.selectBt.addActionListener(self)
        self.backBt.addActionListener(self)

        self.list.addListListener(self)

    def actionPerformed(self, source):
        from src.view.window import Window
        if source == self.addBt:
            self.addT()
            # Window().update()
        elif source == self.editBt:
            self.editT()
            # Window().update()
        elif source == self.removeBt:
            self.removeT()
            # Window().update()
        elif source == self.selectBt:
            self.selectT()
            # Window().update()
        elif source == self.backBt:
            self.onBackBt()

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

    @abstractmethod
    def onBackBt(self):
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
        self.onListValueChanged()
        from src.view.window import Window
        # Window().update()

    @abstractmethod
    def onListValueChanged(self):
        pass
