# TODO: stocke l'integralite des prises presentent sur la portion de mur, et les pistes associées
from src.model.components.handle import Handle
from src.model import database


class Wall:

    def __init__(self, name=None):
        self.id = None
        self.name = name
        self.__paths = None
        self.__handles = None


    def getHandles(self):
        if not self.__handles:
            self.__handles = database.Database().getHandlesInWall(self)

        return self.__handles

    def setHandles(self, handles):
        self.__handles = handles
        database.Database().setHandlesInWall(self.__handles, self)
