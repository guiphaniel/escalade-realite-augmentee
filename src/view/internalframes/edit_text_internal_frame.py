from src.utils.events.event_manager import EventManager
from src.view.internalframes.AbstractInternalFrame import AbstractInternalFrame
from src.view.items.button import Button
from src.view.items.edit_text import EditText
from src.view.listeners.action_listener import ActionListener


class EditTextInternalFrame(AbstractInternalFrame, ActionListener):

    def __init__(self, parent, coordinates, text, bgColor = (240, 240, 240), bgImage = None):
        super().__init__(parent, coordinates, bgColor, bgImage)
        self.text = text

        self.editText = EditText(self, 0, 0, self.text)
        self.add(self.editText)
        self.backBt = Button(self, 0, self.editText.rect.h + 20, text="RETOUR")
        self.add(self.backBt)
        self.validBt = Button(self, self.backBt.rect.w + 20, self.editText.rect.h + 20, text="VALIDER")
        self.add(self.validBt)

        self.shrinkToFit()

        self.backBt.addActionListener(self)
        self.validBt.addActionListener(self)

        self.editTextListeners = []

    def actionPerformed(self, source):
        if source == self.backBt or source == self.validBt:
            EventManager().removeMouseListener(self.backBt)
            EventManager().removeMouseListener(self.validBt)
            EventManager().removeMouseListener(self)
            EventManager().removeMotionListener(self)

        if source == self.backBt:
            self.text = self.editText.initialText
            self.parent.remove(self)
        elif source == self.validBt:
            self.text = self.editText.text
            self.parent.remove(self)
            self.notifyAllEditTextListeners()

    def addEditTextListener(self, l):
        self.editTextListeners.append(l)

    def removeEditTextListener(self, l):
        self.editTextListeners.remove(l)

    def notifyAllEditTextListeners(self):
        for l in self.editTextListeners:
            l.onEditTextResult(self)