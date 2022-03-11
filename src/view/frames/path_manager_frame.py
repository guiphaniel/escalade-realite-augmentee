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
from src.view.frames.player_manager_frame import PlayerManagerFrame
from src.view.items.list_item import ListItem
from src.view.items.text import Text


class PathManagerFrame(AbstractManagerFrame, KeyboardListener):

    def __init__(self):
        AbstractManagerFrame.__init__(self)
        KeyboardListener.__init__(self)
        self.add(Text(40, 50, "Selectionnez un parcours", (0, 0, 0), 120))
        self.list.items = [ListItem(p) for p in Database().getPathsInWall(None)]

    def addT(self):
        path = Path()
        Database().setPathsInWall(self.paths + [path], None)
        listItem = ListItem(path)
        listItem.parent = self.list
        self.list.items.append(listItem)

    def editT(self):
        Database().setPathsInWall(self.paths, None)
        SwitchFrameController().execute(frame=PathCreationFrame, frameArgs={"path": self.list.selectedItem.obj})

    def removeT(self):
        self.list.items.remove(self.list.selectedItem)
        self.list.selectedItem = None
        Database().setPathsInWall(self.paths, None)

    def selectT(self):
        if self.list.selectedItem.obj.getHandles():
            SwitchFrameController().execute(frame=PlayerManagerFrame, frameArgs={"path": self.list.selectedItem.obj})

    def onBackBt(self):
        self.__onBack()

    def __onBack(self):
        from src.view.frames.games_frame import GamesFrame
        SwitchFrameController().execute(frame=GamesFrame)

    @property
    def paths(self):
        return [i.obj for i in self.list.items]

    def onListValueChanged(self):
        if self.list.selectedItem and not self.list.selectedItem.obj.getHandles():
            self.selectBt.active = False

    def onKeyboardEvent(self, e) -> bool:
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.__onBack()
            return True

        return False
