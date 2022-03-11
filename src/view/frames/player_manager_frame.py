import pygame

from src.controllers.games.path_game import PathGame
from src.controllers.start_game_controller import StartGameController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.model.components.path import Path
from src.model.components.player import Player
from src.model.database import Database
from src.utils.events.keyboard_listener import KeyboardListener
from src.view.frames.abstract_manager_frame import AbstractManagerFrame
from src.view.frames.path_creation_frame import PathCreationFrame
from src.view.frames.path_frame import PathFrame
from src.view.internalframes.edit_text_internal_frame import EditTextInternalFrame
from src.view.items.list_item import ListItem
from src.view.items.text import Text
from src.view.listeners.edit_text_listener import EditTextListener


class PlayerManagerFrame(AbstractManagerFrame, EditTextListener, KeyboardListener):

    def __init__(self, path):
        AbstractManagerFrame.__init__(self)
        EditTextListener.__init__(self)
        KeyboardListener.__init__(self)
        self.add(Text(40, 50, "Selectionnez un grimpeur", (0, 0, 0), 120))
        self.list.items = [ListItem(p) for p in Database().getPlayers()]
        self.editText = None
        self.path = path

    @property
    def players(self):
        return [i.obj for i in self.list.items]

    def addT(self):
        player = Player(None)
        Database().setPlayers(self.players + [player])
        listItem = ListItem(player)
        listItem.parent = self.list
        self.list.items.append(listItem)

    def editT(self):
        if not [e for e in self.items if isinstance(e, EditTextInternalFrame)]:
            pseudo = self.list.selectedItem.obj.pseudo
            self.editText = EditTextInternalFrame((800, 400), pseudo)
            self.editText.addEditTextListener(self)
            self.add(self.editText)

    def removeT(self):
        self.list.items.remove(self.list.selectedItem)
        self.list.selectedItem = None
        Database().setPlayers(self.players)

    def selectT(self):
        SwitchFrameController().execute(frame=PathFrame)
        StartGameController().execute(game=PathGame(self.path, self.list.selectedItem.obj))

    def onBackBt(self):
        self.__onBack()

    def __onBack(self):
        from src.view.frames.path_manager_frame import PathManagerFrame
        SwitchFrameController().execute(frame=PathManagerFrame)

    def onEditTextResult(self, source):
        if source == self.editText:
            self.list.selectedItem.setText(source.text)
            self.list.selectedItem.obj.pseudo = source.text
            Database().setPlayers(self.players)

    def onKeyboardEvent(self, e) -> bool:
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.__onBack()
            return True

        return False
