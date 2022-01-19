#TODO: stocke un nom/id, une liste de prises selectionnees, et une liste de joueurs ayant joué sur ce parcours

class Path:
    def __init__(self, name=None):
        self.id = None
        self.name = name
        self.handles = []
