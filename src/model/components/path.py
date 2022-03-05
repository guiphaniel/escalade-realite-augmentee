from src.model import database


class Path:
    def __init__(self, name=None):
        self.id = None
        self.name = name
        self.__handles = []

    def getHandles(self):
        if not self.__handles:
            self.__handles = database.Database().getHandlesInPath(self)

        return self.__handles

    def setHandles(self, handles):
        self.__handles = handles
        database.Database().setHandlesInPath(self.__handles, self)

    def toString(self):
        return self.name

    # overriding these functions is necessary to put paths as keys in dicts (e.g. for scores)
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not (self == other)
