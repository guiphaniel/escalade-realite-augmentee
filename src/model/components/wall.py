from src.model.components.handle import Handle
from src.model import database


class Wall:

    def __init__(self, name=None):
        self.id = None
        self.name = name
        self.__paths = None
        self.__handles = None

    def getPaths(self):
        if not self.__paths:
            self.__paths = database.Database().getPathsInWall(self)

        return self.__paths

    def setPaths(self, paths):
        self.__paths = paths
        database.Database().setPathsInWall(self.__paths, self)

    def getHandles(self):
        if not self.__handles:
            self.__handles = database.Database().getHandlesInWall(self)

        return self.__handles

    def setHandles(self, handles):
        self.__handles = handles
        database.Database().setHandlesInWall(self.__handles, self)
