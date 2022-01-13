# TODO: stocke l'integralite des prises presentent sur la portion de mur, et les pistes associées

class Wall:
    def __init__(self):
        self.id = None
        self.name = None
        self.paths = []
        self.handles = []

    def __init__(self, name):
        self.id = None
        self.name = name
        self.paths = []
        self.handles = []
