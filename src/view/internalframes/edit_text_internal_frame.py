import pygame

from src.utils.events.event_manager import EventManager
from src.utils.events.keyboard_listener import KeyboardListener
from src.view.internalframes.AbstractInternalFrame import AbstractInternalFrame
from src.view.items.button import Button
from src.view.items.edit_text import EditText
from src.view.listeners.action_listener import ActionListener


class EditTextInternalFrame(AbstractInternalFrame, ActionListener, KeyboardListener):

    def __init__(self, parent, coordinates, text, bgColor = (240, 240, 240), bgImage = None):
        AbstractInternalFrame.__init__(self, parent, coordinates, bgColor, bgImage)
        ActionListener.__init__(self)
        KeyboardListener.__init__(self)
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
        if source == self.backBt:
            self.__onBack()
        elif source == self.validBt:
            self.__onValid()

    def __clearEventManager(self):
        EventManager().removeMouseListener(self.backBt)
        EventManager().removeMouseListener(self.validBt)
        EventManager().removeMouseListener(self)
        EventManager().removeMotionListener(self)
        EventManager().removeKeyboardListener(self)

    def __onBack(self):
        self.__clearEventManager()
        self.text = self.editText.initialText
        self.parent.remove(self)

    def __onValid(self):
        self.__clearEventManager()
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

    def onKeyboardEvent(self, e) -> bool:
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                self.__onValid()
                return True
            elif e.key == pygame.K_ESCAPE:
                self.__onBack()
                return True

        return False