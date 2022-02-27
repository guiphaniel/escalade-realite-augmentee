from src.controllers.games.path_game import PathGame
from src.controllers.start_game_controller import StartGameController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.model.components.path import Path
from src.model.components.player import Player
from src.model.database import Database
from src.view.frames.abstract_manager_frame import AbstractManagerFrame
from src.view.frames.path_creation_frame import PathCreationFrame
from src.view.frames.path_frame import PathFrame
from src.view.items.list_item import ListItem


class PathManagerFrame(AbstractManagerFrame):

    def __init__(self):
        AbstractManagerFrame.__init__(self)
        self.list.items = [ListItem(self.list, p) for p in Database().getPathsInWall(None)]

    def addT(self):
        path = Path()
        Database().setPathsInWall(self.paths + [path], None)
        self.list.items.append(ListItem(self.list, path))

    def editT(self):
        Database().setPathsInWall(self.paths, None)
        pathCreationFrame = PathCreationFrame(self.list.selectedItem.obj)
        SwitchFrameController().execute(frame=pathCreationFrame)

    def removeT(self):
        self.list.items.remove(self.list.selectedItem)
        self.list.selectedItem = None
        Database().setPathsInWall(self.paths, None)

    def selectT(self):
        pathFrame = PathFrame()
        SwitchFrameController().execute(frame=pathFrame)
        StartGameController().execute(game=PathGame(pathFrame, self.list.selectedItem.obj, Player(pathFrame)))

    @property
    def paths(self):
        return [i.obj for i in self.list.items]
